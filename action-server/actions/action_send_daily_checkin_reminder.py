import logging
from datetime import datetime
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.lib.environment import get_env
from actions.lib.exceptions import (
    InvalidExternalEventException,
    ReminderNotFoundException,
)
from actions.lib.hashids_util import create_hashids
from db.base import session_factory
from db.reminder import Reminder

logger = logging.getLogger(__name__)

METADATA_ENTITY_NAME = "metadata"
REMINDER_ID_PROPERTY_NAME = "reminder_id"

CHECKIN_URL_PATTERN_ENV_KEY = "DAILY_CHECKIN_URL_PATTERN"


def _query_reminder(session, reminder_id):
    reminder = session.query(Reminder).get(reminder_id)
    if reminder is None:
        raise ReminderNotFoundException(
            f"Reminder with id '{reminder_id}' does not exist."
        )
    return reminder


class ActionSendDailyCheckInReminder(Action):
    def __init__(self):
        self.url_pattern = get_env(CHECKIN_URL_PATTERN_ENV_KEY)
        self.hashids = create_hashids()

        try:
            # Make sure url pattern contains all required keys
            self.url_pattern.format(reminder_id="1", language="fr")
        except KeyError as exception:
            raise KeyError(
                f"Invalid value for {CHECKIN_URL_PATTERN_ENV_KEY} environment variable ({self.url_pattern})"
            ) from exception

    def name(self) -> Text:
        return "action_send_daily_checkin_reminder"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        metadata = next(tracker.get_latest_entity_values(METADATA_ENTITY_NAME))
        hashed_id = metadata[REMINDER_ID_PROPERTY_NAME]
        reminder_id = self.hashids.decode(hashed_id)[0]

        session = session_factory()
        try:
            reminder = _query_reminder(session, reminder_id)

            self._send_reminder(dispatcher, tracker, reminder, hashed_id)

            reminder.last_reminded_at = datetime.utcnow()
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return []

    def _send_reminder(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        reminder: Reminder,
        hashed_id: str,
    ):
        conversation_id = tracker.sender_id
        first_name = reminder.first_name
        phone_number = reminder.phone_number
        language = reminder.language

        if conversation_id != phone_number:
            raise InvalidExternalEventException(
                f"Phone number does not match sender_id: reminder_id={reminder.id} sender_id={conversation_id} phone_number={phone_number}"
            )

        checkin_url = self.url_pattern.format(reminder_id=hashed_id, language=language)

        logger.debug(
            "Sending daily check-in reminder: checkin_url=%s first_name=%s.",
            checkin_url,
            first_name,
        )

        dispatcher.utter_message(
            template="utter_checkin_reminder",
            first_name=first_name,
            check_in_url=checkin_url,
        )

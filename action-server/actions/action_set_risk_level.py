from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionSetRiskLevel(Action):
    def name(self) -> Text:
        return "action_set_risk_level"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        return [
            SlotSet(
                "risk_level",
                "elevated-covid-risk"
                if tracker.get_slot("age_over_65")
                or tracker.get_slot("contact")
                or tracker.get_slot("symptoms") == "moderate"
                else "common",
            )
        ]
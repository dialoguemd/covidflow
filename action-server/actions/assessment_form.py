from typing import Any, Dict, List, Text, Union

from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

ASSESSMENT_TYPE_SLOT = "assessment_type"
SEVERE_SYMPTOMS_SLOT = "severe_symptoms"
MODERATE_SYMPTOMS_SLOT = "moderate_symptoms"
HAS_FEVER_SLOT = "has_fever"
PROVINCE_SLOT = "province"
AGE_OVER_65_SLOT = "age_over_65"
HAS_COUGH_SLOT = "has_cough"
SYMPTOMS_SLOT = "symptoms"


class AssessmentForm(FormAction):
    def name(self) -> Text:

        return "assessment_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        if tracker.get_slot(SEVERE_SYMPTOMS_SLOT):
            return [ASSESSMENT_TYPE_SLOT, SEVERE_SYMPTOMS_SLOT]
        if tracker.get_slot(MODERATE_SYMPTOMS_SLOT):
            return [
                ASSESSMENT_TYPE_SLOT,
                SEVERE_SYMPTOMS_SLOT,
                HAS_FEVER_SLOT,
                PROVINCE_SLOT,
                AGE_OVER_65_SLOT,
                MODERATE_SYMPTOMS_SLOT,
            ]

        return [
            ASSESSMENT_TYPE_SLOT,
            SEVERE_SYMPTOMS_SLOT,
            HAS_FEVER_SLOT,
            PROVINCE_SLOT,
            AGE_OVER_65_SLOT,
            MODERATE_SYMPTOMS_SLOT,
            HAS_COUGH_SLOT,
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            ASSESSMENT_TYPE_SLOT: [
                self.from_trigger_intent(
                    intent="tested_positive", value="tested_positive"
                ),
                self.from_trigger_intent(intent="suspect", value="suspect"),
                self.from_trigger_intent(
                    intent="checkin_return", value="checkin_return"
                ),
            ],
            AGE_OVER_65_SLOT: [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            SEVERE_SYMPTOMS_SLOT: [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            HAS_FEVER_SLOT: [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            MODERATE_SYMPTOMS_SLOT: [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            HAS_COUGH_SLOT: [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
        }

    def validate_assessment_type(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if value == "checkin_return":
            dispatcher.utter_message(template="utter_returning_for_checkin")
        elif value == "tested_positive":
            dispatcher.utter_message(template="utter_self_isolate_separate_room")
            dispatcher.utter_message(template="utter_dont_leave_home")
            dispatcher.utter_message(template="utter_deliver_food_medications")
            dispatcher.utter_message(template="utter_home_assistance")
            dispatcher.utter_message(template="utter_assess_symptoms")

        return {"assessment_type": value}

    def validate_has_fever(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if tracker.get_slot(ASSESSMENT_TYPE_SLOT) == "checkin_return":
            dispatcher.utter_message(template="utter_self_isolate_reminder")
            dispatcher.utter_message(template="utter_home_assistance")

        return {"has_fever": value}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        symptoms_value = "none"
        if tracker.get_slot(SEVERE_SYMPTOMS_SLOT):
            symptoms_value = "severe"
        elif tracker.get_slot(MODERATE_SYMPTOMS_SLOT):
            symptoms_value = "moderate"
        elif tracker.get_slot(HAS_COUGH_SLOT):
            symptoms_value = "mild"

        return [SlotSet(SYMPTOMS_SLOT, symptoms_value)]

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionTestedPositiveMildModerateSymptomsRecommendations(Action):
    def name(self) -> Text:
        return "action_tested_positive_mild_moderate_symptoms_recommendations"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_symptoms_worsen_emergency_assistance")

        return []

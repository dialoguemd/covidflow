from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionTestedPositiveMaybeCuredFinalRecommendations(Action):
    def name(self) -> Text:
        return "action_tested_positive_maybe_cured_final_recommendations"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_maybe_cured")

        return []

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ExtractPlayMusic(Action):

    def name(self) -> Text:
        return "action_extract_music"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        music_entity = next(tracker.get_latest_entity_values("music_name"), None)
        if not music_entity:
            dispatcher.utter_message(text="What music you want to play?")
        band_entity = next(tracker.get_latest_entity_values("band_name"), None)
        if not band_entity:
            dispatcher.utter_message(text="From what band?")

        return []


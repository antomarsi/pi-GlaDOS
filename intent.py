from rasa.core.agent import Agent


class IntentClassifier():

    def __init__(self, model) -> None:
        self.model = model
        self.intents = []

    def load(self):
        self.agent_nlu = Agent.load(self.model)

    async def find_intent(self, text):
        response = await self.agent_nlu.parse_message(text)
        print("finished intent")
        print(response)
        return {
            "intent": response["intent"]["name"],
            "entities": response["entities"],
            "text": text
        }

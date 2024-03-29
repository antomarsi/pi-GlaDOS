import spacy
from rasa.nlu.training_data import load_data
from rasa.nlu.model import Trainer
from rasa.nlu import config
from rasa.nlu.model import Interpreter

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define a function to extract entities using spaCy
def extract_entities_spacy(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({'start': ent.start_char, 'end': ent.end_char, 'value': ent.text, 'entity': ent.label_})
    return entities

# Load Rasa NLU training data
training_data = load_data("data/nlu.md")

# Configure the Rasa NLU pipeline
pipeline = [
    {"name": "SpacyNLP"},
    {"name": "SpacyTokenizer"},
    {"name": "SpacyFeaturizer"},
    {"name": "CRFEntityExtractor"},
    {"name": "EntitySynonymMapper"},
    {"name": "SklearnIntentClassifier"}
]

# Create a trainer that uses this pipeline
trainer = Trainer(config.load("config.yml"))

# Train the model
interpreter = trainer.train(training_data)

# Test the model
text = "I want to book a flight to New York"
print(interpreter.parse(text))

# Test the spaCy entity extraction
print(extract_entities_spacy(text))
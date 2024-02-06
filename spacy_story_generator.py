import spacy
import random

def generate_story(text):
  """
  Generates a short story based on a given string of text, using spaCy NLP.

  Args:
    text: A string of text to use as inspiration for the story.

  Returns:
    A string containing the generated story.
  """

  # Load spaCy pipeline
  nlp = spacy.load("en_core_web_sm")
#   nlp = spacy.load("en_core_web_trf")

  # Process the text with spaCy
  doc = nlp(text)

  # Extract characters, locations, goals, and relationships with spaCy
  characters = {}
  locations = {}
  goals = []
  for token in doc:
    if token.dep_ == "nsubj":  # Extract subject (potential character)
      characters[token.text] = token.head.text  # Get associated noun phrase
    elif token.dep_ == "dobj" and token.head.pos_ == "VERB":  # Extract object of verb (potential goal)
      goals.append(token.text)
    elif token.pos_ == "PROPN":  # Extract proper nouns (potential locations)
      locations[token.text] = ""

  # Randomly choose elements if not enough extracted
  if not characters:
    characters = {"hero": random.choice(text.split())}
  if not locations:
    locations = {"forest": ""}
  if not goals:
    goals = ["defeat enemy", "find treasure"]

  # Create a basic story template
  story = f"Once upon a time, there was a {random.choice(list(characters.keys()))} named {random.choice(list(characters.values()))} who lived in {random.choice(list(locations.keys()))}."
  if goals:
    story += f" Their goal was to {random.choice(goals)}."

  # Add details based on relationships and original text
  for token in doc:
    if token.dep_ in ("nsubj", "dobj", "pobj"):
      continue  # Skip basic dependencies
    if token.head.text in characters:
      characters[token.head.text] += f" {token.dep_} {token.text}"
    elif token.head.text in locations:
      locations[token.head.text] += f" {token.dep_} {token.text}"

  for name, description in characters.items():
    story += f"\n{name.upper()} {description}."

  for location, description in locations.items():
    story += f"\nIn {location} {description}."

  # Add a random ending
  endings = ["happily ever after", "with a heavy heart", "forever changed"]
  story += f"\nAnd so, the story of {random.choice(list(characters.keys()))} came to an end, {random.choice(endings)}."

  return story

# Example usage
text = "In a world of magic and wonder, a brave knight embarked on a quest to save the kingdom."
story = generate_story(text)
print(story)
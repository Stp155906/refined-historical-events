import json
import requests
from datetime import datetime
import spacy
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define planetary symbolism categories
symbolic_categories = {
    'commerce': ['commerce', 'trade', 'business', 'economy'],
    'communication': ['communication', 'media', 'news', 'speech'],
    'war': ['war', 'conflict', 'battle', 'military'],
    'travel': ['travel', 'exploration', 'migration', 'transportation'],
    'conflict': ['conflict', 'dispute', 'tension', 'hostility'],
    'action': ['action', 'movement', 'activity', 'initiative'],
    'law': ['law', 'legal', 'court', 'justice'],
    'philosophy': ['philosophy', 'thought', 'belief', 'ideology'],
    'expansion': ['expansion', 'growth', 'development', 'increase'],
    'structure': ['structure', 'organization', 'institution', 'framework'],
    'discipline': ['discipline', 'control', 'regulation', 'order'],
    'government': ['government', 'state', 'policy', 'administration'],
    'innovation': ['innovation', 'invention', 'technology', 'discovery'],
    'revolution': ['revolution', 'uprising', 'rebellion', 'change'],
    'spirituality': ['spirituality', 'religion', 'faith', 'belief'],
    'dreams': ['dreams', 'visions', 'aspirations', 'imagination'],
    'illusion': ['illusion', 'deception', 'delusion', 'mirage'],
    'transformation': ['transformation', 'change', 'shift', 'metamorphosis'],
    'power': ['power', 'authority', 'control', 'dominance'],
    'rebirth': ['rebirth', 'renewal', 'revival', 'resurrection']
}

# Function to clean the text
def clean_text(text):
    # Replace unwanted characters
    clean_text = text.replace("\\u2013", "–")  # Replace unicode dash with actual dash
    clean_text = clean_text.replace("\\n", " ")  # Replace newlines with a space
    clean_text = clean_text.replace("==", "")  # Remove "==" sections
    clean_text = clean_text.replace("\\u00", "")  # Remove unnecessary unicode sequences
    clean_text = ' '.join(clean_text.split())  # Remove extra spaces

    return clean_text

# Function to fetch Wikipedia events for a given year
def fetch_wikipedia_events(year):
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=true&titles={year}'
    response = requests.get(url)
    json_data = response.json()

    pages = json_data.get('query', {}).get('pages', {})
    extract = ""
    for page_id in pages:
        if 'extract' in pages[page_id]:
            extract = pages[page_id]['extract']

    return extract.strip() if extract else "No relevant information found."

# Function to categorize events based on symbolic categories
def categorize_events(text):
    doc = nlp(text.lower())
    categorized_events = {category: [] for category in symbolic_categories}

    for sentence in doc.sents:
        clean_sentence = clean_text(sentence.text.strip())

        for category, keywords in symbolic_categories.items():
            if any(keyword in clean_sentence for keyword in keywords):
                categorized_events[category].append(clean_sentence.capitalize())

    # Return only categories with at least one event
    return {k: v for k, v in categorized_events.items() if v}

# Main function to fetch and categorize events for the past 100 years
def main():
    current_year = datetime.now().year
    historical_events = {}

    for year in range(current_year - 100, current_year):
        logging.info(f"Fetching events for the year {year}")
        wikipedia_text = fetch_wikipedia_events(year)
        categorized_events = categorize_events(wikipedia_text)
        historical_events[year] = categorized_events

    # Save cleaned and formatted data to a new JSON file
    with open('cleaned_historical_events_100_years.json', 'w') as f:
        json.dump(historical_events, f, indent=4)

    logging.info("Cleaned data saved to 'cleaned_historical_events_100_years.json'")

if __name__ == "__main__":
    main()

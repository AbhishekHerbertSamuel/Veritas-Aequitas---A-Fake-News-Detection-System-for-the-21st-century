import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pickle

def load_data():
    # Read all columns as strings to avoid Dtype warnings
    fake_news_df = pd.read_csv('Fake.csv', dtype=str)
    true_news_df = pd.read_csv('True.csv', dtype=str)

    # Process date columns if necessary or you can ignore them if not needed
    # fake_news_df['date'] = pd.to_datetime(fake_news_df['date'], errors='coerce')
    # true_news_df['date'] = pd.to_datetime(true_news_df['date'], errors='coerce')

    # Combine title and text into one column for richer features
    fake_news_df['combined_text'] = fake_news_df['title'].fillna('') + " " + fake_news_df['text'].fillna('')
    true_news_df['combined_text'] = true_news_df['title'].fillna('') + " " + true_news_df['text'].fillna('')

    # Create labels
    fake_news_df['label'] = 0  # Fake news
    true_news_df['label'] = 1  # True news

    # Combine datasets
    combined_df = pd.concat([fake_news_df, true_news_df], axis=0, ignore_index=True)

    return combined_df[['combined_text', 'label']]

def train_model(data):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(data['combined_text'], data['label'], test_size=0.2, random_state=42)

    # Create a pipeline with TF-IDF and Naive Bayes
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())

    # Train model
    model.fit(X_train, y_train)

    return model

# Load data, train the model
data = load_data()
model = train_model(data)

# Serialize the trained model
with open('text_classifier.pkl', 'wb') as file:
    pickle.dump(model, file)

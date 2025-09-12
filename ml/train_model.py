import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from joblib import dump

def train_and_save_model(csv_file: str = "data/tasks.csv", model_file: str = "ml/model.joblib"):
    """
    Train a simple text classification model for task priority (high/low) and save it.
    """
    # Step 1: Load CSV data
    df = pd.read_csv(csv_file)
    X = df['task_description']  # Features: task descriptions
    y = df['priority']  # Labels: high/low
    print(f"Loaded {len(df)} tasks from {csv_file}")

    # Step 2: Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train set size: {len(X_train)}, Test set size: {len(X_test)}")

    # Step 3: Create a pipeline: TF-IDF vectorizer + Logistic Regression
    model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=100, stop_words='english')),
        ('clf', LogisticRegression(max_iter=1000))
    ])

    # Step 4: Train the model
    model.fit(X_train, y_train)

    # Step 5: Save the model
    dump(model, model_file)
    print(f"Model trained and saved to {model_file}")

    # Step 6: Check accuracy on test data
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy on test data: {accuracy:.2f}")

    # Step 7: Print predictions for test data
    predictions = model.predict(X_test)
    for desc, pred, actual in zip(X_test, predictions, y_test):
        print(f"Description: {desc}, Predicted: {pred}, Actual: {actual}")

if __name__ == "__main__":
    train_and_save_model()
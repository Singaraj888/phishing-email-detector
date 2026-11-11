import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def create_sample_dataset():
    """
    Creates a sample dataset for demonstration.
    In your actual project, replace or load this from your CSV dataset file 
    (e.g., pd.read_csv('emails.csv')).
    """
    data = {
        'text': [
            "Dear user, your bank account has been suspended. Click here to login and verify your password immediately.",
            "Hey team, let's schedule our project sync meeting for tomorrow at 10 AM.",
            "Urgent! You have won a lottery of $1,000,000. Claim your prize by clicking this link.",
            "Hi John, please find attached the quarterly financial report for review.",
            "Security alert: Someone tried to access your account. Reset your credentials using this secure link.",
            "Reminder: Company picnic is scheduled for this coming Friday afternoon."
        ],
        # 1 = Phishing, 0 = Safe (Legitimate)
        'label': [1, 0, 1, 0, 1, 0] 
    }
    return pd.DataFrame(data)

def main():
    # 1. Load Dataset
    print("Loading dataset...")
    df = create_sample_dataset()
    
    # If loading from a file, use:
    # df = pd.read_csv('path_to_your_dataset.csv')
    
    X = df['text']
    y = df['label']

    # 2. Extract Features using TF-IDF (Analyzes keywords, terms, and URL indicators)
    print("Extracting email features using TF-IDF...")
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    X_features = vectorizer.fit_transform(X)

    # 3. Split Dataset into Training and Testing Sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X_features, y, test_size=0.2, random_state=42
    )

    # 4. Train the Model using Random Forest Classifier
    print("Training the Machine Learning model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 5. Make Predictions
    y_pred = model.predict(X_test)

    # 6. Display Accuracy and Confusion Matrix
    acc = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    print("\n--- Model Evaluation Results ---")
    print(f"Accuracy: {acc * 100:.2f}%")
    print("\nConfusion Matrix:")
    print(conf_matrix)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Example classification of a new email
    print("\n--- Testing a New Email ---")
    new_email = ["Verify your bank details immediately via this link to avoid account closure."]
    new_email_vectorized = vectorizer.transform(new_email)
    prediction = model.predict(new_email_vectorized)
    
    result = "Phishing" if prediction[0] == 1 else "Safe"
    print(f"Email Content: '{new_email[0]}'")
    print(f"Classification Result: {result}")

if __name__ == "__main__":
    main()

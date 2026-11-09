
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

print("PHISHING EMAIL DETECTION SYSTEM")
print("=" * 45)

# 1. Load dataset
df = pd.read_csv("phishing_emails.csv")

# 2. Clean dataset
df = df.dropna(subset=["text_combined", "label"])
df = df.drop_duplicates()

df["text_combined"] = df["text_combined"].astype(str)
df["label"] = pd.to_numeric(df["label"], errors="coerce")
df = df.dropna(subset=["label"])
df["label"] = df["label"].astype(int)

print("\nDataset loaded successfully!")
print("Total records:", len(df))

print("\nLabel distribution:")
print(df["label"].value_counts())

# This dataset uses 0 for legitimate and 1 for phishing.
# Confirm this mapping against the Kaggle dataset description.
if set(df["label"].unique()) != {0, 1}:
    raise ValueError("Expected labels 0 and 1. Check the dataset labels.")

# 3. Separate input and output
X = df["text_combined"]
y = df["label"]

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

# 5. Create machine learning pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            max_features=30000,
            ngram_range=(1, 2),
            min_df=2
        )
    ),
    (
        "classifier",
        LogisticRegression(max_iter=1000)
    )
])

# 6. Train model
print("\nTraining model... Please wait.")
model.fit(X_train, y_train)

# 7. Make predictions
predictions = model.predict(X_test)

# 8. Evaluate model
accuracy = accuracy_score(y_test, predictions)

print("\nMODEL EVALUATION")
print("=" * 45)

print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
report = classification_report(
    y_test,
    predictions,
    target_names=["Legitimate", "Phishing"]
)

print(report)

print("\nConfusion Matrix:")
matrix = confusion_matrix(y_test, predictions)
print(matrix)

# 9. Save trained model
joblib.dump(model, "phishing_model.pkl")

# 10. Save evaluation results
with open("model_results.txt", "w") as file:
    file.write("PHISHING EMAIL DETECTION RESULTS\n")
    file.write("=" * 40 + "\n")
    file.write(f"Accuracy: {accuracy * 100:.2f}%\n\n")
    file.write("Classification Report:\n")
    file.write(report)
    file.write("\nConfusion Matrix:\n")
    file.write(str(matrix))

print("\nModel saved as phishing_model.pkl")
print("Results saved as model_results.txt")
print("\nMODEL TRAINING COMPLETED!")

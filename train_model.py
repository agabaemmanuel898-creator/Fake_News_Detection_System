import pandas as pd
import re
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

import joblib


# Text cleaning function
def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Load the datasets
fake_news = pd.read_csv("dataset/Fake.csv")
real_news = pd.read_csv("dataset/True.csv")


# Add labels
fake_news["label"] = 0
real_news["label"] = 1


# Combine both datasets
data = pd.concat([fake_news, real_news], ignore_index=True)


# Shuffle the data
data = data.sample(frac=1, random_state=42).reset_index(drop=True)


# Clean the news text
data["text"] = data["text"].apply(clean_text)


# Create input (X) and target (y)
X = data["text"]
y = data["label"]


# Split the data into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Convert text into numbers using TF-IDF
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_df=0.7
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


print("Training data converted:", X_train_tfidf.shape)
print("Testing data converted:", X_test_tfidf.shape)


# Train the machine learning model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)


print("Model training completed!")


# Test the model
y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)


# Create confusion matrix
cm = confusion_matrix(y_test, y_pred)

print("Confusion Matrix:")
print(cm)


# Display accuracy and classification report
print("Model Accuracy:", accuracy)
print(classification_report(y_test, y_pred))


# Create visual confusion matrix
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Fake News", "Real News"]
)

disp.plot()

plt.title("Fake News Detection Confusion Matrix")
plt.tight_layout()

# Save confusion matrix as an image
plt.savefig("confusion_matrix.png", dpi=300)

plt.show()


# Save the trained model
joblib.dump(model, "model/fake_news_model.pkl")


# Save the TF-IDF vectorizer
joblib.dump(vectorizer, "model/tfidf_vectorizer.pkl")


print("Model and vectorizer saved successfully!")
print("Confusion matrix saved as confusion_matrix.png")
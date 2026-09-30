import pandas as pd
import joblib
import re
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# Text cleaning function
def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Load the trained model and vectorizer
model = joblib.load("model/fake_news_model.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")


# Load the datasets
fake_news = pd.read_csv("dataset/Fake.csv")
real_news = pd.read_csv("dataset/True.csv")


# Add labels
fake_news["label"] = 0
real_news["label"] = 1


# Select 100 articles from each dataset
fake_test = fake_news.sample(100, random_state=42)
real_test = real_news.sample(100, random_state=42)


# Combine the test articles
test_data = pd.concat(
    [fake_test, real_test],
    ignore_index=True
)


# Clean the text
test_data["text"] = test_data["text"].apply(clean_text)


# Prepare input and actual labels
X_test = test_data["text"]
y_test = test_data["label"]


# Convert text into TF-IDF
X_test_tfidf = vectorizer.transform(X_test)


# Make predictions
y_pred = model.predict(X_test_tfidf)


# Get prediction probabilities
probabilities = model.predict_proba(X_test_tfidf)

confidence = probabilities.max(axis=1) * 100


# Add prediction results to the test data
test_data["actual_label"] = y_test
test_data["predicted_label"] = y_pred
test_data["confidence"] = confidence.round(2)


# Convert labels into readable names
test_data["actual_result"] = test_data["actual_label"].map({
    0: "Fake News",
    1: "Real News"
})

test_data["predicted_result"] = test_data["predicted_label"].map({
    0: "Fake News",
    1: "Real News"
})


# Show whether each prediction was correct
test_data["correct"] = (
    test_data["actual_label"] == test_data["predicted_label"]
)


# Save test results to CSV
test_data.to_csv(
    "test_results.csv",
    index=False
)


# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)


print("\n===== MODEL TEST RESULTS =====")
print("Number of articles tested:", len(test_data))
print("Accuracy:", accuracy)
print("Accuracy percentage:", round(accuracy * 100, 2), "%")


# Display confusion matrix
print("\nConfusion Matrix:")

cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)


# Create visual confusion matrix

plt.figure(figsize=(6, 5))

plt.imshow(
    cm,
    interpolation="nearest"
)

plt.title(
    "Fake News Detection - 200 Article Test"
)

plt.colorbar()

plt.xticks(
    [0, 1],
    ["Fake News", "Real News"]
)

plt.yticks(
    [0, 1],
    ["Fake News", "Real News"]
)

plt.xlabel(
    "Predicted Label"
)

plt.ylabel(
    "Actual Label"
)


# Add numbers inside the matrix

for i in range(2):

    for j in range(2):

        plt.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center"
        )


plt.tight_layout()

plt.savefig(
    "test_confusion_matrix.png",
    dpi=300
)

plt.show()

print(
    "\nTest confusion matrix saved as: test_confusion_matrix.png"
)


# Display classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


print("\nDetailed test results saved as: test_results.csv")
from flask import Flask, render_template, request
import joblib
import re
from news_search import search_news

app = Flask(__name__)


# Text cleaning function
def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Load the trained model and TF-IDF vectorizer
model = joblib.load("model/fake_news_model.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check_news():

    try:

        news_text = request.form.get("news_text", "")

        cleaned_text = clean_text(news_text)

        news_tfidf = vectorizer.transform(
            [cleaned_text]
        )

        prediction = model.predict(
            news_tfidf
        )[0]

        probabilities = model.predict_proba(
            news_tfidf
        )[0]

        confidence = max(probabilities) * 100

        if prediction == 0:
            result = "FAKE NEWS"
        else:
            result = "REAL NEWS"

        return f"{result}|{confidence:.2f}"

    except Exception as error:

        print("Prediction error:", error)

        return "ERROR|Prediction could not be completed", 500

@app.route("/search-news", methods=["POST"])
def online_news_search():

    try:

        news_text = request.form.get("news_text", "").strip()

        if not news_text:
            return {"results": []}

        # Use the first 20 words as the search query
        search_query = " ".join(news_text.split()[:20])

        results = search_news(
            search_query,
            max_results=5
        )

        return {"results": results}

    except Exception as error:

        print("Online search error:", error)

        return {"results": []}

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
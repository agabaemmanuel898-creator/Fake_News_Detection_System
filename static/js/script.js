const newsText = document.getElementById("newsText");
const prediction = document.getElementById("prediction");
const confidence = document.getElementById("confidence");
const explanation = document.getElementById("explanation");
const resultBox = document.getElementById("resultBox");
const charCount = document.getElementById("charCount");
const themeButton = document.getElementById("themeButton");
const checkButton = document.getElementById("checkButton");
const confidenceBar = document.getElementById("confidenceBar");
const onlineResults = document.getElementById("onlineResults");
const onlineStatus = document.getElementById("onlineStatus");
const newsSources = document.getElementById("newsSources");


// ========================================
// Character Counter
// ========================================

newsText.addEventListener("input", function () {

    const length = newsText.value.length;

    charCount.textContent =
    "Characters: " +
    length +
    " | Minimum: 30 | Maximum: 5000";

    if (length < 30) {

    charCount.style.color =
        "#d00000";

}

else if (length >= 4500) {

    charCount.style.color =
        "#d97706";

}

else {

    charCount.style.color =
        "#008a20";

}

});


// ========================================
// Check News
// ========================================

checkButton.addEventListener(
    "click",
    async function () {

        const article = newsText.value.trim();


        // Check empty input
        if (article === "") {

            prediction.textContent =
                "Please enter a news article before checking.";

            confidence.textContent = "";
            explanation.textContent = "";

            prediction.style.color = "#555";
            resultBox.style.backgroundColor = "#f2f2f2";

            confidenceBar.style.width = "0%";

            return;
        }


        // Check if article is too short
        if (article.length < 30) {

            prediction.textContent =
                "Article is too short. Please enter at least 30 characters";

            confidence.textContent =
                "Please enter more details.";

            explanation.textContent = "";

            prediction.style.color = "#d00000";
            resultBox.style.backgroundColor = "#ffe5e5";

            confidenceBar.style.width = "0%";

            return;
        }


        // Loading message
        prediction.textContent =
            "Checking news...";

        checkButton.textContent =
            "Checking...";
            checkButton.classList.add("checking");
            checkButton.disabled = true;

        confidence.textContent = "";
        explanation.textContent = "";
        confidenceBar.style.width = "0%";

        prediction.style.color = "#555";
        resultBox.style.backgroundColor = "#f2f2f2";

        confidenceBar.style.width = "0%";


        try {

            // Keep checking message visible for 5 seconds
            await new Promise(
                resolve => setTimeout(resolve, 5000)
            );


            // Send news to Flask
            const response = await fetch(
                "/check",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    },

                    body:
                        "news_text=" +
                        encodeURIComponent(article)
                }
            );


            // Check server response
            if (!response.ok) {

                throw new Error(
                    "Server error: " +
                    response.status
                );

            }


            // Get response
            const data =
                await response.text();


            // Separate prediction and confidence
            const parts =
                data.split("|");


            const result =
                parts[0];

            const confidenceValue =
                parts[1];

                searchOnlineNews(newsText.value);


            // Display prediction
            prediction.textContent =
                result;

            checkButton.textContent =
                "Check News";
                checkButton.classList.remove("checking");
                checkButton.disabled = false;

            confidence.textContent =
                "Confidence: " +
                confidenceValue +
                "%";


            // Display confidence bar
            confidenceBar.style.width =
                confidenceValue + "%";


            // Display explanation
            if (result === "FAKE NEWS") {

                explanation.textContent =
                    "The model identified patterns commonly associated with fake news in its training data. This prediction does not independently verify the article's factual accuracy.";

                prediction.style.color =
                    "#d00000";

                resultBox.style.backgroundColor =
                    "#ffe5e5";

                confidenceBar.style.backgroundColor =
                    "#d00000";

            }


            else if (result === "REAL NEWS") {

                explanation.textContent =
                    "The model identified patterns commonly associated with real news in its training data. This prediction does not independently verify the article's factual accuracy.";

                prediction.style.color =
                    "#008a20";

                resultBox.style.backgroundColor =
                    "#e5ffe9";

                confidenceBar.style.backgroundColor =
                    "#008a20";

            }

        }


        catch (error) {

            console.error(
                "Prediction error:",
                error
            );


            prediction.textContent =
                "Something went wrong.";
                checkButton.textContent =
                "Check News";

            checkButton.classList.remove("checking");
            checkButton.disabled = false;

            confidence.textContent =
                "Please make sure the system is running and try again.";

            explanation.textContent = "";

            prediction.style.color =
                "#d00000";

            resultBox.style.backgroundColor =
                "#ffe5e5";

            confidenceBar.style.width =
                "0%";

            checkButton.textContent =
                "Check News";

        }

    }
);


// ========================================
// Clear News
// ========================================

document
    .getElementById("clearButton")
    .addEventListener(
        "click",
        function () {

            newsText.value = "";

            prediction.textContent = "";
            confidence.textContent = "";
            explanation.textContent = "";
            onlineStatus.textContent = "Search results will appear here.";
            newsSources.innerHTML = "";
            onlineResults.style.display = "none";

            charCount.textContent =
    "Characters: 0 | Minimum: 30 | Maximum: 5000";

            charCount.style.color =
                "#d00000";

            resultBox.style.backgroundColor =
                "#f2f2f2";

            confidenceBar.style.width =
                "0%";

            confidenceBar.style.backgroundColor =
                "#008a20";

            checkButton.textContent =
                "Check News";

        }
    );


// ========================================
// Dark Mode
// ========================================

const savedTheme =
    localStorage.getItem("theme");


if (savedTheme === "dark") {

    document.body.classList.add(
        "dark-mode"
    );

    themeButton.textContent =
        "☀️ Light";

}


themeButton.addEventListener(
    "click",
    function () {

        document.body.classList.toggle(
            "dark-mode"
        );


        if (
            document.body.classList.contains(
                "dark-mode"
            )
        ) {

            themeButton.textContent =
                "☀️ Light";

            localStorage.setItem(
                "theme",
                "dark"
            );

        }

        else {

            themeButton.textContent =
                "🌙 Dark";

            localStorage.setItem(
                "theme",
                "light"
            );

        }

    }
);
// ========================================
// Back to Top
// ========================================

const backToTop =
    document.getElementById("backToTop");


window.addEventListener(
    "scroll",
    function () {

        if (window.scrollY > 400) {

            backToTop.style.display =
                "flex";

        }

        else {

            backToTop.style.display =
                "none";

        }

    }
);


backToTop.addEventListener(
    "click",
    function () {

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }
);
     async function searchOnlineNews(articleText) {

      onlineResults.style.display = "block";
      onlineStatus.textContent = "Searching for related news reports...";
      newsSources.innerHTML = "";

    try {

        const response = await fetch("/search-news", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                news_text: articleText
            })
        });

        const data = await response.json();

        if (!data.results || data.results.length === 0) {

            onlineStatus.textContent =
                "No related news reports were found.";

            return;
        }

        onlineStatus.textContent =
            "Related news reports found:";

        data.results.forEach(function (article) {

            const articleDiv = document.createElement("div");

            articleDiv.className = "news-source";

            articleDiv.innerHTML = `
                <h4>${article.title}</h4>
                <p>
                    Source: ${article.source || "Unknown source"}
                </p>
                <a href="${article.link}"
                   target="_blank"
                   rel="noopener noreferrer">
                    Read source
                </a>
            `;

            newsSources.appendChild(articleDiv);

        });

    } catch (error) {

        console.error("Online search error:", error);

        onlineStatus.textContent =
            "Online search could not be completed.";
    }
}
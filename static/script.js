
const emailInput = document.getElementById("email");
const charCount = document.getElementById("charCount");
const result = document.getElementById("result");
const analyzeBtn = document.getElementById("analyzeBtn");

emailInput.addEventListener("input", () => {
    charCount.textContent =
        `${emailInput.value.length} / 100000`;
});

async function analyzeEmail() {
    const email = emailInput.value.trim();

    if (!email) {
        result.className = "result error";
        result.textContent = "Please enter email content first.";
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analysing...";
    result.className = "result";
    result.style.display = "block";
    result.textContent = "Please wait while the email is analysed.";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analysis failed.");
        }

        const phishing = data.prediction ===
            "Potential Phishing Email";

        result.className = phishing
            ? "result danger"
            : "result safe";

        const heading = document.createElement("strong");
        heading.textContent = data.prediction;

        const probability = document.createElement("p");
        probability.textContent =
            `Phishing probability: ${data.phishing_probability}%`;

        const note = document.createElement("small");
        note.textContent =
            "Automated prediction only. This result does not guarantee email safety.";

        result.replaceChildren(heading, probability, note);

    } catch (error) {
        result.className = "result error";
        result.textContent = error.message;
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyse Email →";
    }
}

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("voiceForm");
    const resultContainer = document.getElementById("resultContainer");

    if (!form) return;

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        resultContainer.classList.remove("hidden");
        resultContainer.innerHTML = "<p>Analyzing voice...</p>";

        const formData = new FormData(form);

        try {

            const response = await fetch("/api/voice", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (!data.success) {

                resultContainer.innerHTML = `
                    <div class="card">
                        <h3>Analysis Failed</h3>
                        <p>${data.message}</p>
                    </div>
                `;

                return;
            }

            const result = data.result;

            resultContainer.innerHTML = `

                <div class="card">

                    <h2>Voice Investigation Result</h2>

                    <hr>

                    <p><strong>Prediction:</strong> ${result.prediction}</p>

                    <p><strong>Risk Level:</strong> ${result.risk}</p>

                    <p><strong>Risk Score:</strong> ${result.risk_score}%</p>

                    <p><strong>Confidence:</strong> ${result.confidence}%</p>

                    <p><strong>Detected Language:</strong> ${result.language || "Unknown"}</p>

                    <hr>

                    <h3>Transcript</h3>

                    <div class="mt-2">
                        ${result.transcript || "No transcript available."}
                    </div>

                </div>

            `;

        } catch (error) {

            resultContainer.innerHTML = `
                <div class="card">
                    <h3>Error</h3>
                    <p>${error.message}</p>
                </div>
            `;
        }

    });

});
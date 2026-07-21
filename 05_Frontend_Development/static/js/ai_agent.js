document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("agentForm");
    const resultBox = document.getElementById("agentResult");

    if (!form) return;

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        resultBox.classList.remove("hidden");
        resultBox.innerHTML = "<p>Investigating...</p>";

        const query = document.getElementById("query").value.trim();

        try {

            const response = await fetch("/api/agent/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    query: query
                })
            });

            const data = await response.json();

            if (!data.success) {

                resultBox.innerHTML = `
                    <div class="card">
                        <h3>Request Failed</h3>
                        <p>${data.message}</p>
                    </div>
                `;
                return;
            }

            const result = data.result;
            const explanation = data.explanation;

            resultBox.innerHTML = `
                <div class="card">

                    <h2>Investigation Result</h2>

                    <hr>

                    <p><strong>Query:</strong> ${result.query}</p>

                    <p><strong>Confidence:</strong> ${explanation.confidence}%</p>

                    <p><strong>Summary:</strong></p>

                    <div class="mt-2 mb-4">
                        ${explanation.summary}
                    </div>

                    <h3>Evidence</h3>

                    <ul class="mt-2">

                        ${explanation.evidence.map(item => `
                                <li>
                                    <strong>${item.source}</strong>
                                    (${item.category})
                                    - Score:
                                    ${item.relevance_score}
                                </li>
                            `).join("")
                }

                    </ul>

                </div>
            `;

        } catch (error) {

            resultBox.innerHTML = `
                <div class="card">
                    <h3>Error</h3>
                    <p>${error.message}</p>
                </div>
            `;

        }

    });

});
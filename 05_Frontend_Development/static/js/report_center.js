document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("reportForm");
    const result = document.getElementById("reportResult");

    if (!form) return;

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        result.innerHTML = "Generating report...";

        const payload = {
            case_id: document.getElementById("caseId").value.trim(),
            format: document.getElementById("reportFormat").value
        };

        try {

            const response = await fetch("/api/report/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!data.success) {

                result.innerHTML = `
                    <div class="card">
                        <h3>Generation Failed</h3>
                        <p>${data.message}</p>
                    </div>
                `;

                return;
            }

            result.innerHTML = `
                <div class="card">

                    <h3>Report Generated Successfully</h3>

                    <p><strong>Case ID:</strong> ${data.case_id}</p>

                    <p><strong>Format:</strong> ${data.format.toUpperCase()}</p>

                    <p><strong>Status:</strong> ${data.status}</p>

                    ${data.download_url
                    ? `<a class="btn btn-primary mt-4" href="${data.download_url}">
                                   Download Report
                               </a>`
                    : ""
                }

                </div>
            `;

        } catch (error) {

            result.innerHTML = `
                <div class="card">
                    <h3>Error</h3>
                    <p>${error.message}</p>
                </div>
            `;

        }

    });

});
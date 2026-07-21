document.addEventListener("DOMContentLoaded", () => {

    const caseList = document.getElementById("caseList");
    const searchButton = document.getElementById("searchButton");

    async function loadCases() {

        const query = document.getElementById("searchBox").value.trim();
        const risk = document.getElementById("riskFilter").value;

        let url = "/api/cases";

        const params = new URLSearchParams();

        if (query) {
            params.append("query", query);
        }

        if (risk) {
            params.append("risk", risk);
        }

        if (params.toString()) {
            url += "?" + params.toString();
        }

        caseList.innerHTML = "Loading...";

        try {

            const response = await fetch(url);
            const data = await response.json();

            if (!data.success) {
                caseList.innerHTML = data.message;
                return;
            }

            if (!data.cases.length) {
                caseList.innerHTML = "No cases found.";
                return;
            }

            caseList.innerHTML = data.cases.map(caseItem => `

                <div class="card mb-4">

                    <h3>${caseItem.case_id}</h3>

                    <p><strong>Risk:</strong> ${caseItem.risk}</p>

                    <p><strong>Status:</strong> ${caseItem.status}</p>

                    <p><strong>Created:</strong> ${caseItem.created_at}</p>

                </div>

            `).join("");

        } catch (error) {

            caseList.innerHTML = error.message;

        }

    }

    searchButton.addEventListener("click", loadCases);

    loadCases();

});
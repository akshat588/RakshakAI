document.addEventListener("DOMContentLoaded", async () => {

    const totalInvestigations = document.getElementById("totalInvestigations");
    const highRiskCases = document.getElementById("highRiskCases");
    const campaigns = document.getElementById("campaigns");
    const iocCount = document.getElementById("iocCount");
    const activityFeed = document.getElementById("activityFeed");

    try {

        const response = await fetch("/api/dashboard");

        const data = await response.json();

        if (!data.success) {
            activityFeed.innerHTML = "<p>Unable to load dashboard.</p>";
            return;
        }

        const dashboard = data.dashboard;

        totalInvestigations.textContent = dashboard.total_investigations ?? 0;
        highRiskCases.textContent = dashboard.high_risk_cases ?? 0;
        campaigns.textContent = dashboard.active_campaigns ?? 0;
        iocCount.textContent = dashboard.total_iocs ?? 0;

        if (
            dashboard.recent_activity &&
            dashboard.recent_activity.length
        ) {

            activityFeed.innerHTML =
                dashboard.recent_activity.map(item => `
                    <div class="border-b py-3">
                        <strong>${item.title}</strong>
                        <div>${item.description}</div>
                        <small>${item.time}</small>
                    </div>
                `).join("");

        } else {

            activityFeed.innerHTML =
                "<p>No recent activity available.</p>";

        }

        if (window.Chart && dashboard.risk_distribution) {

            const ctx = document
                .getElementById("riskChart")
                .getContext("2d");

            new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: Object.keys(dashboard.risk_distribution),
                    datasets: [{
                        data: Object.values(
                            dashboard.risk_distribution
                        )
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });

        }

    } catch (error) {

        activityFeed.innerHTML =
            `<p>${error.message}</p>`;

    }

});
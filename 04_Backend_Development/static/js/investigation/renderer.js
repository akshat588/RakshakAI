/*
===============================================================================
RakshakAI
Universal Investigation Renderer
===============================================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    const container = document.getElementById("investigation-container");

    if (!container) return;

    const stored = sessionStorage.getItem("investigation_result");

    if (!stored) {

        container.innerHTML = `
            <div class="glass rounded-3xl p-8 text-center">

                <h2 class="text-2xl font-bold mb-4">
                    No Investigation Found
                </h2>

                <p class="text-muted">
                    Please perform a scan first.
                </p>

            </div>
        `;

        return;

    }

    const result = InvestigationHelpers.normalize(
        JSON.parse(stored)
    );

    const config =
        InvestigationConfig[result.analyzer] ||
        InvestigationConfig.default;

    container.innerHTML = "";

    container.appendChild(
        InvestigationHero.render(result, config)
    );

    container.appendChild(
        InvestigationSummary.render(result, config)
    );

    container.appendChild(
        InvestigationTimeline.render(config)
    );

    container.appendChild(
        InvestigationDetails.render(result, config)
    );

    container.appendChild(
        InvestigationExplanation.render(result)
    );

    container.appendChild(
        InvestigationIndicators.render(result)
    );

    container.appendChild(
        InvestigationRecommendations.render(result)
    );

    container.appendChild(
        InvestigationActions.render()
    );

});
/*
===============================================================================
RakshakAI
Universal Investigation Summary Component
===============================================================================
*/

window.InvestigationSummary = (() => {

    const H = window.InvestigationHelpers;

    function createCard(title, value) {

        const card = H.create(
            "div",
            "glass rounded-3xl p-7"
        );

        card.innerHTML = `
            <p class="text-muted">

                ${title}

            </p>

            <h2 class="text-3xl font-bold mt-5 break-words">

                ${value}

            </h2>
        `;

        return card;

    }

    function render(result, config) {

        const grid = H.create(
            "div",
            "grid xl:grid-cols-4 md:grid-cols-2 gap-6 mb-8"
        );

        grid.appendChild(
            createCard(
                "Threat Score",
                H.formatPercentage(result.confidence)
            )
        );

        grid.appendChild(
            createCard(
                "Risk Level",
                result.risk
            )
        );

        grid.appendChild(
            createCard(
                "AI Confidence",
                H.formatPercentage(result.confidence)
            )
        );

        grid.appendChild(
            createCard(
                "Detection Engine",
                config.engine
            )
        );

        return grid;

    }

    return {

        render

    };

})();
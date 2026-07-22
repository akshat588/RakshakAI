/*
===============================================================================
RakshakAI
Universal Investigation Hero Component
===============================================================================
*/

window.InvestigationHero = (() => {

    const H = window.InvestigationHelpers;

    function render(result, config) {

        const badgeStyle = H.riskClass(result.risk).badge;

        const container = H.create(
            "div",
            "glass rounded-3xl p-8 mb-8"
        );

        container.innerHTML = `
            <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">

                <div>

                    <span class="badge badge-primary">

                        ${config.heroBadge}

                    </span>

                    <h1 class="text-4xl font-bold mt-4">

                        ${result.prediction}

                    </h1>

                    <p class="text-muted mt-3 max-w-3xl">

                        ${config.reportDescription}

                    </p>

                </div>

                <div class="text-right">

                    <span class="px-6 py-3 rounded-full font-bold text-lg ${badgeStyle}">

                        ${result.risk} RISK

                    </span>

                </div>

            </div>
        `;

        return container;

    }

    return {

        render

    };

})();
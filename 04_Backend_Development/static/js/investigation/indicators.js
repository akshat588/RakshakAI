/*
===============================================================================
RakshakAI
Universal Threat Indicators Component
===============================================================================
*/

window.InvestigationIndicators = (() => {

    const H = window.InvestigationHelpers;

    function render(result) {

        const card = H.create(
            "div",
            "glass rounded-3xl p-7"
        );

        const title = H.create(
            "h3",
            "text-xl font-bold mb-6",
            "Threat Indicators"
        );

        card.appendChild(title);

        if (!result.indicators.length) {

            const empty = H.create(
                "div",
                "text-green-400",
                "No threat indicators detected."
            );

            card.appendChild(empty);

            return card;

        }

        const list = H.create(
            "div",
            "space-y-3"
        );

        result.indicators.forEach(indicator => {

            const item = H.create(
                "div",
                "border border-red-500/20 bg-red-500/5 rounded-2xl p-4 flex items-start gap-3"
            );

            item.innerHTML = `
                <span class="text-red-400 text-lg">⚠️</span>

                <span class="flex-1">
                    ${indicator}
                </span>
            `;

            list.appendChild(item);

        });

        card.appendChild(list);

        return card;

    }

    return {

        render

    };

})();
/*
===============================================================================
RakshakAI
Universal Security Recommendations Component
===============================================================================
*/

window.InvestigationRecommendations = (() => {

    const H = window.InvestigationHelpers;

    function render(result) {

        const card = H.create(
            "div",
            "glass rounded-3xl p-7"
        );

        const title = H.create(
            "h3",
            "text-xl font-bold mb-6",
            "Security Recommendations"
        );

        card.appendChild(title);

        if (!result.recommendations.length) {

            const empty = H.create(
                "div",
                "text-green-400",
                "No additional recommendations available."
            );

            card.appendChild(empty);

            return card;

        }

        const list = H.create(
            "div",
            "space-y-3"
        );

        result.recommendations.forEach((recommendation, index) => {

            const item = H.create(
                "div",
                "border border-green-500/20 bg-green-500/5 rounded-2xl p-4 flex items-start gap-4"
            );

            item.innerHTML = `
                <div class="flex-shrink-0 w-8 h-8 rounded-full bg-green-500 text-black font-bold flex items-center justify-center">
                    ${index + 1}
                </div>

                <div class="flex-1">
                    ${recommendation}
                </div>
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
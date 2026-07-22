/*
===============================================================================
RakshakAI
Universal Explainable AI Component
===============================================================================
*/

window.InvestigationExplanation = (() => {

    const H = window.InvestigationHelpers;

    function render(result) {

        const card = H.create(
            "div",
            "glass rounded-3xl p-7"
        );

        const title = H.create(
            "h3",
            "text-xl font-bold mb-6",
            "Explainable AI"
        );

        card.appendChild(title);

        if (!result.explanation.length) {

            const empty = H.create(
                "div",
                "text-green-400",
                "No explanation available."
            );

            card.appendChild(empty);

            return card;

        }

        result.explanation.forEach(item => {

            const explanation = H.create(
                "div",
                "border border-blue-500/20 bg-blue-500/5 rounded-2xl p-4 mb-3"
            );

            explanation.innerHTML = `
                <div class="flex gap-3">

                    <span>🤖</span>

                    <span>${item}</span>

                </div>
            `;

            card.appendChild(explanation);

        });

        return card;

    }

    return {

        render

    };

})();
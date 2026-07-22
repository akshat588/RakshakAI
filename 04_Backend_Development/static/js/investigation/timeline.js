/*
===============================================================================
RakshakAI
Universal Investigation Timeline Component
===============================================================================
*/

window.InvestigationTimeline = (() => {

    const H = window.InvestigationHelpers;

    function render(config) {

        const card = H.create(
            "div",
            "glass rounded-3xl p-7 mb-8"
        );

        const title = H.create(
            "h3",
            "text-2xl font-bold mb-6",
            "Investigation Timeline"
        );

        const list = H.create(
            "div",
            "space-y-4"
        );

        (config.timeline || []).forEach((step, index) => {

            const item = H.create(
                "div",
                "flex items-start gap-4 border-l-2 border-cyan-500 pl-4 py-2"
            );

            item.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-cyan-500 text-black flex items-center justify-center font-bold">

                    ${index + 1}

                </div>

                <div>

                    <p class="font-semibold">

                        ${step}

                    </p>

                </div>
            `;

            list.appendChild(item);

        });

        card.appendChild(title);
        card.appendChild(list);

        return card;

    }

    return {

        render

    };

})();
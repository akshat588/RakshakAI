/*
===============================================================================
RakshakAI
Universal Investigation Actions Component
===============================================================================
*/

window.InvestigationActions = (() => {

    const H = window.InvestigationHelpers;

    function render() {

        const container = H.create(
            "div",
            "glass rounded-3xl p-7 mt-8"
        );

        const title = H.create(
            "h3",
            "text-xl font-bold mb-6",
            "Actions"
        );

        container.appendChild(title);

        const buttonContainer = H.create(
            "div",
            "flex flex-wrap gap-4"
        );

        const buttons = [

            {
                text: "🔄 Scan Again",
                className: "btn btn-primary",
                onClick: () => window.history.back()
            },

            {
                text: "🏠 Dashboard",
                className: "btn btn-secondary",
                onClick: () => {
                    window.location.href = "/";
                }
            },

            {
                text: "📄 Download Report",
                className: "btn btn-outline",
                onClick: () => window.print()
            },

            {
                text: "📋 Copy Results",
                className: "btn btn-outline",
                onClick: () => {

                    navigator.clipboard.writeText(
                        document.body.innerText
                    );

                    alert("Investigation report copied to clipboard.");

                }
            }

        ];

        buttons.forEach(button => {

            const btn = H.create(
                "button",
                button.className,
                button.text
            );

            btn.type = "button";
            btn.addEventListener("click", button.onClick);

            buttonContainer.appendChild(btn);

        });

        container.appendChild(buttonContainer);

        return container;

    }

    return {

        render

    };

})();
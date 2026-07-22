/*
===============================================================================
RakshakAI
Universal Investigation Details Component
===============================================================================
*/

window.InvestigationDetails = (() => {

    const H = window.InvestigationHelpers;

    function createRow(label, value) {

        const row = H.create(
            "div",
            "flex justify-between items-start gap-4 py-2 border-b border-slate-700 last:border-b-0"
        );

        row.innerHTML = `
            <span class="text-muted">

                ${label}

            </span>

            <span class="text-right break-all">

                ${value}

            </span>
        `;

        return row;

    }

    function render(result, config) {

        const card = H.create(
            "div",
            "glass rounded-3xl p-7"
        );

        const title = H.create(
            "h3",
            "text-xl font-bold mb-6",
            "Investigation Details"
        );

        card.appendChild(title);

        card.appendChild(
            createRow(
                "Prediction",
                result.prediction
            )
        );

        card.appendChild(
            createRow(
                "Risk Level",
                result.risk
            )
        );

        card.appendChild(
            createRow(
                "AI Confidence",
                H.formatPercentage(result.confidence)
            )
        );

        card.appendChild(
            createRow(
                "Detection Engine",
                config.engine
            )
        );

        card.appendChild(
            createRow(
                "Scan ID",
                result.scan_id
            )
        );

        card.appendChild(
            createRow(
                "Timestamp",
                result.timestamp
            )
        );

        if (result.metadata &&
            Object.keys(result.metadata).length > 0) {

            const heading = H.create(
                "h4",
                "text-lg font-semibold mt-8 mb-4",
                "Additional Information"
            );

            card.appendChild(heading);

            Object.entries(result.metadata).forEach(([key, value]) => {

                card.appendChild(
                    createRow(
                        key.replace(/_/g, " "),
                        value ?? "-"
                    )
                );

            });

        }

        return card;

    }

    return {

        render

    };

})();
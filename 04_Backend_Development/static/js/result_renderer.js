/*
==========================================================
RakshakAI Result Rendering Engine
Version : 1.0
==========================================================
*/

const RESULT_ENGINE = {

    getThreatScore(data) {

        if (data.risk_score != null)
            return Math.round(Number(data.risk_score));

        if (data.confidence != null)
            return Math.round(Number(data.confidence));

        return 0;
    },

    getBadge(risk) {

        switch (risk) {

            case "CRITICAL":
                return "bg-danger text-white";

            case "HIGH":
                return "bg-danger/20 text-danger";

            case "MEDIUM":
                return "bg-warning/20 text-warning";

            default:
                return "bg-success/20 text-success";

        }

    },

    getConfidence(data) {

        if (data.confidence == null)
            return "Unavailable";

        return Number(data.confidence).toFixed(2) + "%";

    }

};
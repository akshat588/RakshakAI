/*
===============================================================================
RakshakAI
Universal Investigation Helper Library
===============================================================================
*/

window.InvestigationHelpers = (() => {

    function safeArray(value) {

        if (Array.isArray(value)) return value;

        if (value === null || value === undefined) return [];

        if (typeof value === "string") {

            const text = value.trim();

            return text ? [text] : [];
        }

        return [];
    }

    function safeNumber(value, fallback = 0) {

        const num = Number(value);

        return Number.isFinite(num) ? num : fallback;
    }

    function formatPercentage(value) {

        return `${safeNumber(value).toFixed(2)}%`;

    }

    function riskClass(risk) {

        switch ((risk || "").toUpperCase()) {

            case "CRITICAL":
            case "HIGH":

                return {
                    badge: "bg-red-500/20 text-red-400 border border-red-500/30",
                    color: "text-red-400"
                };

            case "MEDIUM":

                return {
                    badge: "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30",
                    color: "text-yellow-400"
                };

            case "LOW":

                return {
                    badge: "bg-blue-500/20 text-blue-400 border border-blue-500/30",
                    color: "text-blue-400"
                };

            default:

                return {
                    badge: "bg-green-500/20 text-green-400 border border-green-500/30",
                    color: "text-green-400"
                };

        }

    }

    function normalize(result = {}) {

        return {

            analyzer:
                result.analyzer || "Unknown",

            prediction:
                result.prediction ||
                result.result ||
                "Analysis Completed",

            confidence:
                safeNumber(
                    result.confidence ??
                    result.risk_score
                ),

            risk:
                result.risk || "LOW",

            scan_id:
                result.scan_id || "-",

            timestamp:
                result.timestamp ||
                new Date().toLocaleString(),

            explanation:
                safeArray(
                    result.explanation ||
                    result.evidence
                ),

            indicators:
                safeArray(
                    result.indicators ||
                    result.flags ||
                    result.iocs
                ),

            recommendations:
                safeArray(
                    result.recommendations ||
                    result.recommendation
                ),

            metadata:
                result.metadata || {}

        };

    }

    function create(tag, className = "", html = "") {

        const element = document.createElement(tag);

        if (className) {

            element.className = className;

        }

        if (html) {

            element.innerHTML = html;

        }

        return element;

    }

    return {

        safeArray,
        safeNumber,
        formatPercentage,
        riskClass,
        normalize,
        create

    };

})();
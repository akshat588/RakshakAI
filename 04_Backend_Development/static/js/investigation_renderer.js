function getRiskBadge(risk) {

    switch ((risk || "").toUpperCase()) {

        case "HIGH":
        case "CRITICAL":
            return "bg-red-500/20 text-red-400 border border-red-500/30";

        case "MEDIUM":
            return "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30";

        case "LOW":
            return "bg-blue-500/20 text-blue-400 border border-blue-500/30";

        default:
            return "bg-green-500/20 text-green-400 border border-green-500/30";
    }

}

function safeArray(value) {

    if (Array.isArray(value)) return value;

    if (typeof value === "string" && value.trim() !== "") {

        return [value];

    }

    return [];

}

function createCards(items, icon, classes) {

    let html = "";

    safeArray(items).forEach(item => {

        html += `
        <div class="${classes} rounded-2xl p-4 mb-3">

            <div class="flex gap-3">

                <span>${icon}</span>

                <span>${item}</span>

            </div>

        </div>
        `;

    });

    return html;

}

function getExplanation(result) {

    return createCards(

        result.explanation,

        "🤖",

        "border border-blue-500/20 bg-blue-500/5"

    );

}

function getIndicators(result) {

    return createCards(

        result.indicators,

        "⚠",

        "border border-red-500/20 bg-red-500/5"

    );

}

function getRecommendations(result) {

    return createCards(

        result.recommendations,

        "✓",

        "border border-green-500/20 bg-green-500/5"

    );

}

function formatPercentage(value) {

    if (value === undefined || value === null) {

        return 0;

    }

    return Number(value).toFixed(2);

}

function normalizeResult(result) {

    return {

        analyzer: result.analyzer || "Unknown",

        prediction: result.prediction || result.result || "Analysis Completed",

        confidence: Number(result.confidence ?? result.risk_score ?? 0),

        risk: result.risk || "LOW",

        scan_id: result.scan_id || "-",

        timestamp: result.timestamp || new Date().toLocaleString(),

        explanation: result.explanation || result.evidence || [],

        indicators: result.flags || result.iocs || [],

        recommendations:
            result.recommendation ||
            result.recommendations ||
            []

    };

}

function renderInvestigation(result) {

    result = normalizeResult(result);

    const analyzer = result.analyzer || "Email";

    const cfg = INVESTIGATION_CONFIG[analyzer];

    if (!cfg) {

        console.error("No configuration found for:", analyzer);

        return;

    }

    document.getElementById("heroBadge").textContent = cfg.heroBadge;

    document.getElementById("heroTitle").textContent = cfg.reportTitle;

    document.getElementById("heroDescription").textContent = cfg.reportDescription;

    document.getElementById("engineName").textContent = cfg.engine;

    const badge = getRiskBadge(result.risk);

    const explanation =
        getExplanation(result) ||
        `<p class="text-green-400">No explanation available.</p>`;

    const indicators =
        getIndicators(result) ||
        `<p class="text-green-400">No indicators detected.</p>`;

    const recommendations =
        getRecommendations(result) ||
        `<p class="text-green-400">No recommendations available.</p>`;

    const timeline = cfg.timeline
        .map((step, index) => `<div>${index + 1}. ${step}</div>`)
        .join("");

    document.getElementById("resultContainer").innerHTML = `
<div class="space-y-8">

<div class="glass rounded-3xl p-8">

<div class="flex justify-between items-center flex-wrap gap-5">

<div>

<span class="badge badge-primary">

Executive Summary

</span>

<h2 class="text-3xl font-bold mt-4">

${result.prediction}

</h2>

<p class="text-muted mt-3">

RakshakAI successfully completed the AI investigation.

</p>

</div>

<div>

<span class="px-6 py-3 rounded-full font-bold text-lg ${badge}">

${result.risk} RISK

</span>

</div>

</div>

</div>

<div class="grid xl:grid-cols-4 md:grid-cols-2 gap-6">

<div class="glass rounded-3xl p-7">

<p class="text-muted">Threat Score</p>

<h2 class="text-5xl font-bold mt-3">

${formatPercentage(result.confidence)}%

</h2>

</div>

<div class="glass rounded-3xl p-7">

<p class="text-muted">Risk Level</p>

<h2 class="text-3xl font-bold mt-5">

${result.risk}

</h2>

</div>

<div class="glass rounded-3xl p-7">

<p class="text-muted">AI Confidence</p>

<h2 class="text-3xl font-bold mt-5">

${formatPercentage(result.confidence)}%

</h2>

</div>

<div class="glass rounded-3xl p-7">

<p class="text-muted">Detection Engine</p>

<h2 class="text-2xl font-bold mt-5">

${cfg.engine}

</h2>

</div>

</div>

<div class="glass rounded-3xl p-7">

<h3 class="text-2xl font-bold mb-6">

Investigation Timeline

</h3>

<div class="space-y-4">

${timeline}

</div>

</div>

<div class="grid xl:grid-cols-2 gap-6">

<div class="glass rounded-3xl p-7">

<h3 class="text-xl font-bold mb-6">

Investigation Details

</h3>

<div class="space-y-4">

<div class="flex justify-between">

<span class="text-muted">Prediction</span>

<span>${result.prediction}</span>

</div>

<div class="flex justify-between">

<span class="text-muted">Risk</span>

<span>${result.risk || "-"}</span>

</div>

<div class="flex justify-between">

<span class="text-muted">Confidence</span>

<span>${formatPercentage(result.confidence)}%</span>

</div>

<div class="flex justify-between">

<span class="text-muted">Engine</span>

<span>${cfg.engine}</span>

</div>

<div class="flex justify-between">

<span class="text-muted">Scan ID</span>

<span>${result.scan_id}</span>

</div>

<div class="flex justify-between">

<span class="text-muted">Timestamp</span>

<span>${result.timestamp}</span>

</div>

</div>

</div>

<div class="glass rounded-3xl p-7">

<h3 class="text-xl font-bold mb-6">

Explainable AI

</h3>

${explanation}

</div>

</div>

<div class="glass rounded-3xl p-7">

<h3 class="text-xl font-bold mb-6">

${cfg.indicatorTitle}

</h3>

${indicators}

</div>

<div class="glass rounded-3xl p-7">

<h3 class="text-xl font-bold mb-6">

${cfg.recommendationTitle}

</h3>

${recommendations}

</div>

<div class="flex flex-wrap gap-4">

<button id="newScan" class="bg-primary text-black font-bold px-6 py-3 rounded-2xl">

🔄 New Investigation

</button>

<button id="copyBtn" class="glass px-6 py-3 rounded-2xl">

📋 Copy Report

</button>

<button id="exportBtn" class="glass px-6 py-3 rounded-2xl">

⬇ Export JSON

</button>

</div>

</div>
`;

    document.getElementById("newScan").onclick = () => {

        sessionStorage.removeItem("investigation_result");

        history.back();

    };

    document.getElementById("copyBtn").onclick = () => {

        navigator.clipboard.writeText(
            JSON.stringify(result, null, 2)
        );

        showToast(
            "Report copied successfully.",
            "success"
        );

    };

    document.getElementById("exportBtn").onclick = () => {

        const blob = new Blob(
            [JSON.stringify(result, null, 4)],
            { type: "application/json" }
        );

        const a = document.createElement("a");

        a.href = URL.createObjectURL(blob);

        a.download = `${analyzer}_Investigation_Report.json`;

        a.click();

    };

}
/*
==========================================================
RakshakAI v2
Universal AI Security Assistant
==========================================================
Author : RakshakAI
Version: 2.0
==========================================================
*/

"use strict";

class RakshakAIAssistant {

    constructor() {

        /* ===========================
           Configuration
        =========================== */

        this.config = {

            api: "/api/assistant",

            typingDelay: 500,

            toastDuration: 4000,

            maxHistory: 25,

            maxAttachments: 10

        };

        /* ===========================
           Runtime State
        =========================== */

        this.state = {

            loading: false,

            attachments: [],

            history: [],

            lastReport: null,

            autoScroll: true

        };

        /* ===========================
           DOM Cache
        =========================== */

        this.ui = {};

    }

    /* =====================================================
       INITIALIZATION
    ===================================================== */

    init() {

        this.cacheDOM();

        this.bindEvents();

        this.initializeHistory();

        this.updateCharacterCounter();

        console.log("RakshakAI Assistant Initialized");

    }

    /* =====================================================
       DOM CACHE
    ===================================================== */

    cacheDOM() {

        this.ui.chat =
            document.getElementById("chatMessages");

        this.ui.input =
            document.getElementById("userInput");

        this.ui.send =
            document.getElementById("sendBtn");

        this.ui.clear =
            document.getElementById("clearBtn");

        this.ui.voice =
            document.getElementById("voiceBtn");

        this.ui.upload =
            document.getElementById("uploadBtn");

        this.ui.file =
            document.getElementById("fileInput");

        this.ui.preview =
            document.getElementById(
                "attachmentPreview"
            );

        this.ui.counter =
            document.getElementById(
                "charCounter"
            );

        this.ui.loading =
            document.getElementById(
                "loadingOverlay"
            );

        this.ui.typing =
            document.getElementById(
                "typingIndicator"
            );

        this.ui.report =
            document.getElementById(
                "reportContainer"
            );

        this.ui.placeholder =
            document.getElementById(
                "reportPlaceholder"
            );

    }


    /* =====================================================
       EVENT BINDING
    ===================================================== */

    bindEvents() {

        this.ui.send?.addEventListener(
            "click",
            () => this.sendMessage()
        );

        this.ui.clear?.addEventListener(
            "click",
            () => this.clearInput()
        );

        this.ui.input?.addEventListener(
            "input",
            () => this.updateCharacterCounter()
        );

        this.ui.input?.addEventListener(
            "keydown",
            e => {

                if (
                    e.key === "Enter" &&
                    !e.shiftKey
                ) {

                    e.preventDefault();

                    this.sendMessage();

                }

            }
        );

        this.ui.upload?.addEventListener(
            "click",
            () => this.ui.file.click()
        );

        this.ui.file?.addEventListener(
            "change",
            e => {

                this.addAttachments(
                    [...e.target.files]
                );

            }
        );

    }

    /* =====================================================
       CHARACTER COUNTER
    ===================================================== */

    updateCharacterCounter() {

        const length =
            this.ui.input.value.length;

        this.ui.counter.textContent =
            `${length} Characters`;

    }

    /* =====================================================
       INPUT
    ===================================================== */

    clearInput() {

        this.ui.input.value = "";

        this.updateCharacterCounter();

    }

    getInput() {

        return this.ui.input.value.trim();

    }

    /* =====================================================
       ATTACHMENTS
    ===================================================== */

    addAttachments(files) {

        files.forEach(file => {

            if (
                this.state.attachments.length >=
                this.config.maxAttachments
            ) {

                this.showToast(
                    "Maximum attachments reached.",
                    "warning"
                );

                return;

            }

            this.state.attachments.push(file);

            this.renderAttachment(file);

        });

    }

    renderAttachment(file) {

        const chip =
            document.createElement("div");

        chip.className =
            "attachment-chip";

        chip.innerHTML = `

        <span>

            📎 ${file.name}

        </span>

        <button>

            ×

        </button>

    `;

        chip
            .querySelector("button")
            .addEventListener(
                "click",
                () => {

                    this.state.attachments =
                        this.state.attachments.filter(
                            f => f !== file
                        );

                    chip.remove();

                }
            );

        this.ui.preview.appendChild(chip);

    }

    /* =====================================================
       CHAT RENDERING
    ===================================================== */

    addUserMessage(content) {

        const template =
            document
                .getElementById(
                    "userMessageTemplate"
                )
                .content
                .cloneNode(true);

        template.querySelector(
            ".message-content"
        ).textContent = content;

        template.querySelector(
            ".message-time"
        ).textContent =
            this.getCurrentTime();

        this.ui.chat.appendChild(template);

        this.scrollToBottom();

    }

    addAssistantMessage(content) {

        const template =
            document
                .getElementById(
                    "assistantMessageTemplate"
                )
                .content
                .cloneNode(true);

        template.querySelector(
            ".message-content"
        ).textContent = content;

        template.querySelector(
            ".message-time"
        ).textContent =
            this.getCurrentTime();

        this.ui.chat.appendChild(template);

        this.scrollToBottom();

    }

    addAssistantHTML(html) {

        const template =
            document
                .getElementById(
                    "assistantMessageTemplate"
                )
                .content
                .cloneNode(true);

        template.querySelector(
            ".message-content"
        ).innerHTML = html;

        template.querySelector(
            ".message-time"
        ).textContent =
            this.getCurrentTime();

        this.ui.chat.appendChild(template);

        this.scrollToBottom();

    }

    /* =====================================================
       HELPERS
    ===================================================== */

    getCurrentTime() {

        return new Date().toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit"
            }
        );

    }

    scrollToBottom() {

        if (!this.state.autoScroll)
            return;

        this.ui.chat.scrollTo({

            top:
                this.ui.chat.scrollHeight,

            behavior: "smooth"

        });

    }

    /* =====================================================
       LOADING
    ===================================================== */

    showLoading(message = "Running AI Investigation...") {

        document.getElementById(
            "loadingStatus"
        ).textContent = message;

        this.ui.loading.classList.remove(
            "hidden"
        );

    }

    hideLoading() {

        this.ui.loading.classList.add(
            "hidden"
        );

    }

    showTyping() {

        this.ui.typing.classList.remove(
            "hidden"
        );

        this.scrollToBottom();

    }

    hideTyping() {

        this.ui.typing.classList.add(
            "hidden"
        );

    }

    /* =====================================================
       API CLIENT
    ===================================================== */

    async sendMessage() {

        const content = this.getInput();

        if (
            content.length === 0 &&
            this.state.attachments.length === 0
        ) {

            this.showToast(
                "Please enter some content.",
                "warning"
            );

            return;

        }

        this.addUserMessage(content);

        this.showTyping();

        this.showLoading();

        this.state.loading = true;

        try {

            const response = await fetch(
                this.config.api,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        content

                    })

                }
            );

            const data =
                await response.json();

            this.hideTyping();

            this.hideLoading();

            this.state.loading = false;

            if (!response.ok || !data.success) {

                throw new Error(

                    data.error ||
                    data.message ||
                    "Investigation failed."

                );

            }

            this.state.lastReport =
                data.report;

            this.renderInvestigation(
                data.report
            );

            this.saveHistory(
                data.report
            );

            this.clearInput();

        }

        catch (error) {

            console.error(error);

            this.hideTyping();

            this.hideLoading();

            this.state.loading = false;

            this.addAssistantMessage(

                "Unable to complete the investigation."

            );

            this.showToast(

                error.message,

                "error"

            );

        }

    }

    /* =====================================================
       INVESTIGATION REPORT RENDERER
    ===================================================== */

    renderInvestigation(report) {

        this.ui.placeholder.classList.add(
            "hidden"
        );

        this.ui.report.classList.remove(
            "hidden"
        );

        this.renderSummary(report);

        this.renderThreatScore(report);

        this.renderConfidence(report);

        this.renderEvidence(report);

        this.renderIOCs(report);

        this.renderRecommendations(report);

        this.renderTimeline(report);

        this.addAssistantMessage(

            `${report.status}\n\n${report.result}`

        );

    }

    renderSummary(report) {

        document.getElementById(
            "summaryContent"
        ).innerHTML = `

        <p><strong>Analyzer:</strong>
            ${report.analyzer}
        </p>

        <p><strong>Status:</strong>
            ${report.status}
        </p>

        <p><strong>Prediction:</strong>
            ${report.prediction}
        </p>

        <p><strong>Result:</strong>
            ${report.result}
        </p>

        <p><strong>Risk:</strong>

            <span class="risk-badge risk-${report.risk.toLowerCase()}">

                ${report.risk}

            </span>

        </p>

    `;

    }

    renderThreatScore(report) {

        document.getElementById(
            "threatScore"
        ).innerHTML = `

        <div class="score-circle">

            ${Math.round(report.risk_score)}

        </div>

        <div class="score-label">

            Threat Score

        </div>

    `;

    }

    renderConfidence(report) {

        document.getElementById(
            "confidenceBar"
        ).innerHTML = `

        <div class="confidence-track">

            <div
                class="confidence-fill"
                style="width:${report.confidence}%">

            </div>

        </div>

        <div class="confidence-value">

            ${report.confidence.toFixed(2)}%

        </div>

    `;

    }

    /* =====================================================
       EVIDENCE
    ===================================================== */

    renderEvidence(report) {

        const container =
            document.getElementById(
                "evidenceList"
            );

        container.innerHTML = "";

        const evidence =
            report.evidence || [];

        if (evidence.length === 0) {

            container.innerHTML = `

            <div class="empty-history">

                No evidence available.

            </div>

        `;

            return;

        }

        evidence.forEach(item => {

            const template =
                document
                    .getElementById(
                        "evidenceItemTemplate"
                    )
                    .content
                    .cloneNode(true);

            template.querySelector(
                ".chip-title"
            ).textContent = item;

            container.appendChild(template);

        });

    }

    /* =====================================================
       INDICATORS OF COMPROMISE
    ===================================================== */

    renderIOCs(report) {

        const container =
            document.getElementById(
                "iocList"
            );

        container.innerHTML = "";

        const iocs =
            report.iocs ||
            report.indicators ||
            [];

        if (iocs.length === 0) {

            container.innerHTML = `

            <div class="empty-history">

                No indicators found.

            </div>

        `;

            return;

        }

        iocs.forEach(item => {

            const template =
                document
                    .getElementById(
                        "iocTemplate"
                    )
                    .content
                    .cloneNode(true);

            template.querySelector(
                ".ioc-value"
            ).textContent = item;

            container.appendChild(template);

        });

    }

    /* =====================================================
       RECOMMENDATIONS
    ===================================================== */

    renderRecommendations(report) {

        const container =
            document.getElementById(
                "recommendationList"
            );

        container.innerHTML = "";

        const recommendations =
            report.recommendations || [];

        if (recommendations.length === 0) {

            container.innerHTML = `

            <div class="empty-history">

                No recommendations available.

            </div>

        `;

            return;

        }

        recommendations.forEach(item => {

            const template =
                document
                    .getElementById(
                        "recommendationTemplate"
                    )
                    .content
                    .cloneNode(true);

            template.querySelector(
                ".recommendation-text"
            ).textContent = item;

            container.appendChild(template);

        });

    }

    /* =====================================================
       TIMELINE
    ===================================================== */

    renderTimeline(report) {

        const container =
            document.getElementById(
                "timelineContainer"
            );

        container.innerHTML = "";

        const timeline =
            report.timeline || [];

        if (timeline.length === 0) {

            container.innerHTML = `

            <div class="empty-history">

                Investigation completed.

            </div>

        `;

            return;

        }

        timeline.forEach(item => {

            const template =
                document
                    .getElementById(
                        "timelineItemTemplate"
                    )
                    .content
                    .cloneNode(true);

            template.querySelector(
                ".timeline-text"
            ).textContent = item;

            container.appendChild(template);

        });

    }

    /* =====================================================
       HISTORY MANAGER
    ===================================================== */

    saveHistory(report) {

        this.state.history.unshift({

            timestamp:
                report.timestamp,

            analyzer:
                report.analyzer,

            result:
                report.result,

            risk:
                report.risk,

            confidence:
                report.confidence

        });

        if (
            this.state.history.length >
            this.config.maxHistory
        ) {

            this.state.history.pop();

        }

        this.renderHistory();

    }

    initializeHistory() {

        this.renderHistory();

    }

    renderHistory() {

        const container =
            document.getElementById(
                "recentInvestigations"
            );

        container.innerHTML = "";

        if (
            this.state.history.length === 0
        ) {

            container.innerHTML = `

            <div class="empty-history">

                No Investigations Yet

            </div>

        `;

            return;

        }

        this.state.history.forEach(item => {

            const card =
                document.createElement("div");

            card.className =
                "scan-card";

            card.innerHTML = `

            <div class="scan-title">

                ${item.analyzer.toUpperCase()}

            </div>

            <div class="scan-time">

                ${item.result}

            </div>

            <div class="scan-time">

                ${item.risk}

                •

                ${item.confidence.toFixed(1)}%

            </div>

        `;

            container.appendChild(card);

        });

    }

    /* =====================================================
       TOASTS
    ===================================================== */

    showToast(
        message,
        type = "success"
    ) {

        const container =
            document.getElementById(
                "toastContainer"
            );

        const toast =
            document.createElement("div");

        toast.className =
            `toast ${type}`;

        toast.innerHTML = `

        <strong>

            ${type.toUpperCase()}

        </strong>

        <div>

            ${message}

        </div>

    `;

        container.appendChild(toast);

        setTimeout(() => {

            toast.remove();

        }, this.config.toastDuration);

    }

    /* =====================================================
       DRAG & DROP
    ===================================================== */

    initializeDragDrop() {

        const overlay =
            document.getElementById(
                "dragOverlay"
            );

        ["dragenter", "dragover"].forEach(event => {

            document.addEventListener(
                event,
                e => {

                    e.preventDefault();

                    overlay.classList.remove(
                        "hidden"
                    );

                }
            );

        });

        ["dragleave", "dragend", "drop"].forEach(event => {

            document.addEventListener(
                event,
                e => {

                    e.preventDefault();

                    overlay.classList.add(
                        "hidden"
                    );

                }
            );

        });

        document.addEventListener(
            "drop",
            e => {

                const files =
                    [...e.dataTransfer.files];

                if (!files.length)
                    return;

                this.addAttachments(files);

            }
        );

    }

    /* =====================================================
       IMAGE PREVIEW
    ===================================================== */

    previewImage(file) {

        if (
            !file.type.startsWith("image/")
        )
            return;

        const reader =
            new FileReader();

        reader.onload = event => {

            const chip =
                document.createElement("div");

            chip.className =
                "attachment-chip";

            chip.innerHTML = `

            <img
                src="${event.target.result}"
                width="40"
                height="40"
                style="
                    border-radius:8px;
                    object-fit:cover;
                ">

            <span>

                ${file.name}

            </span>

        `;

            this.ui.preview.appendChild(
                chip
            );

        };

        reader.readAsDataURL(file);

    }

    /* =====================================================
       FILE MANAGER
    ===================================================== */

    initializeUploads() {

        this.initializeDragDrop();

        this.ui.file?.addEventListener(
            "change",
            event => {

                [...event.target.files]
                    .forEach(file => {

                        this.previewImage(file);

                    });

            }
        );

    }

    /* =====================================================
       EXPORT MANAGER
    ===================================================== */

    initializeExports() {

        document
            .getElementById("exportJson")
            ?.addEventListener(
                "click",
                () => this.exportJSON()
            );

        document
            .getElementById("copyReport")
            ?.addEventListener(
                "click",
                () => this.copyReport()
            );

    }

    exportJSON() {

        if (!this.state.lastReport) {

            this.showToast(
                "No investigation report available.",
                "warning"
            );

            return;

        }

        const blob = new Blob(

            [
                JSON.stringify(
                    this.state.lastReport,
                    null,
                    4
                )
            ],

            {
                type: "application/json"
            }

        );

        const url =
            URL.createObjectURL(blob);

        const link =
            document.createElement("a");

        link.href = url;

        link.download =
            `RakshakAI_Report_${Date.now()}.json`;

        document.body.appendChild(link);

        link.click();

        document.body.removeChild(link);

        URL.revokeObjectURL(url);

        this.showToast(
            "JSON report exported successfully.",
            "success"
        );

    }

    copyReport() {

        if (!this.state.lastReport) {

            this.showToast(
                "No report available.",
                "warning"
            );

            return;

        }

        navigator.clipboard
            .writeText(

                JSON.stringify(
                    this.state.lastReport,
                    null,
                    2
                )

            )
            .then(() => {

                this.showToast(
                    "Report copied to clipboard.",
                    "success"
                );

            })
            .catch(() => {

                this.showToast(
                    "Unable to copy report.",
                    "error"
                );

            });

    }

    /* =====================================================
       MODAL MANAGER
    ===================================================== */

    initializeModals() {

        document
            .querySelectorAll(".close-modal")
            .forEach(button => {

                button.addEventListener(
                    "click",
                    () => {

                        const modal =
                            document.getElementById(
                                button.dataset.close
                            );

                        if (modal) {

                            modal.classList.add(
                                "hidden"
                            );

                        }

                    }
                );

            });

    }

    openModal(id) {

        const modal =
            document.getElementById(id);

        if (!modal)
            return;

        modal.classList.remove(
            "hidden"
        );

    }

    closeModal(id) {

        const modal =
            document.getElementById(id);

        if (!modal)
            return;

        modal.classList.add(
            "hidden"
        );

    }

    /* =====================================================
       FLOATING ACTIONS
    ===================================================== */

    initializeFloatingButtons() {

        document
            .getElementById(
                "scrollBottomBtn"
            )
            ?.addEventListener(
                "click",
                () => this.scrollToBottom()
            );

        document
            .getElementById(
                "newChatBtn"
            )
            ?.addEventListener(
                "click",
                () => this.newInvestigation()
            );

    }

    newInvestigation() {

        this.ui.chat.innerHTML = "";

        this.ui.placeholder.classList.remove(
            "hidden"
        );

        this.ui.report.classList.add(
            "hidden"
        );

        this.state.lastReport = null;

        this.state.attachments = [];

        this.ui.preview.innerHTML = "";

        this.clearInput();

        this.showToast(
            "New investigation started.",
            "success"
        );

    }

    /* =====================================================
       KEYBOARD SHORTCUTS
    ===================================================== */

    initializeKeyboardShortcuts() {

        document.addEventListener(
            "keydown",
            event => {

                /* Ctrl + Enter = Analyze */

                if (
                    event.ctrlKey &&
                    event.key === "Enter"
                ) {

                    event.preventDefault();

                    this.sendMessage();

                }

                /* Escape = Clear Input */

                if (event.key === "Escape") {

                    this.clearInput();

                }

            }
        );

    }

    /* =====================================================
       GLOBAL HELPERS
    ===================================================== */

    resetAssistant() {

        this.state.loading = false;

        this.state.attachments = [];

        this.ui.preview.innerHTML = "";

        this.hideLoading();

        this.hideTyping();

        this.clearInput();

    }

    destroy() {

        this.resetAssistant();

        this.state.history = [];

        this.state.lastReport = null;

    }

    debug() {

        console.group(
            "RakshakAI Debug"
        );

        console.log(
            "State:",
            this.state
        );

        console.log(
            "Config:",
            this.config
        );

        console.log(
            "UI:",
            this.ui
        );

        console.groupEnd();

    }

    /* =====================================================
       APPLICATION BOOTSTRAP
    ===================================================== */

    initializeModules() {

        this.initializeUploads();

        this.initializeExports();

        this.initializeModals();

        this.initializeFloatingButtons();

        this.initializeKeyboardShortcuts();

    }

    boot() {

        this.initializeModules();

        this.showToast(

            "RakshakAI Assistant Ready",

            "success"

        );

        console.log(
            "%cRakshakAI v2",
            "color:#2563eb;font-size:15px;font-weight:bold;"
        );

        console.log(
            "Universal AI Security Assistant Ready"
        );

        console.log(
            "Backend:",
            this.config.api
        );

    }

    /* =====================================================
       REPORT UTILITIES
    ===================================================== */

    formatRiskBadge(risk) {

        if (!risk)
            return "risk-low";

        switch (String(risk).toUpperCase()) {

            case "CRITICAL":
                return "risk-critical";

            case "HIGH":
                return "risk-high";

            case "MEDIUM":
                return "risk-medium";

            default:
                return "risk-low";

        }

    }

    formatPercentage(value) {

        const number = Number(value);

        if (Number.isNaN(number))
            return "0.00%";

        return `${number.toFixed(2)}%`;

    }

    escapeHTML(text) {

        const div =
            document.createElement("div");

        div.textContent =
            text ?? "";

        return div.innerHTML;

    }

    clearReport() {

        this.ui.placeholder.classList.remove(
            "hidden"
        );

        this.ui.report.classList.add(
            "hidden"
        );

        document.getElementById(
            "summaryContent"
        ).innerHTML = "";

        document.getElementById(
            "threatScore"
        ).innerHTML = "";

        document.getElementById(
            "confidenceBar"
        ).innerHTML = "";

        document.getElementById(
            "evidenceList"
        ).innerHTML = "";

        document.getElementById(
            "iocList"
        ).innerHTML = "";

        document.getElementById(
            "recommendationList"
        ).innerHTML = "";

        document.getElementById(
            "timelineContainer"
        ).innerHTML = "";

    }

    /* =====================================================
       SESSION MANAGER
    ===================================================== */

    saveSession() {

        try {

            localStorage.setItem(

                "rakshakai_session",

                JSON.stringify({

                    history: this.state.history,

                    lastReport: this.state.lastReport

                })

            );

        }

        catch (error) {

            console.warn(
                "Unable to save session.",
                error
            );

        }

    }

    restoreSession() {

        try {

            const session =
                localStorage.getItem(
                    "rakshakai_session"
                );

            if (!session)
                return;

            const data =
                JSON.parse(session);

            this.state.history =
                data.history || [];

            this.state.lastReport =
                data.lastReport || null;

            this.renderHistory();

            if (this.state.lastReport) {

                this.renderInvestigation(
                    this.state.lastReport
                );

            }

        }

        catch (error) {

            console.warn(
                "Unable to restore session.",
                error
            );

        }

    }

    /* =====================================================
       LIFECYCLE
    ===================================================== */

    beforeUnload() {

        this.saveSession();

    }

    registerLifecycleEvents() {

        window.addEventListener(

            "beforeunload",

            () => this.beforeUnload()

        );

    }

    /* =====================================================
       APPLICATION ENTRY POINT
    ===================================================== */

    start() {

        this.restoreSession();

        this.registerLifecycleEvents();

        this.boot();

        console.log(
            "%cRakshakAI Universal AI Security Assistant",
            "color:#2563eb;font-size:16px;font-weight:bold;"
        );

        console.log(
            "Application Started Successfully."
        );

    }

}

/* =====================================================
   CREATE SINGLE APPLICATION INSTANCE
===================================================== */

const RakshakAI = new RakshakAIAssistant();

/* =====================================================
   DOM READY
===================================================== */

document.addEventListener(

    "DOMContentLoaded",

    () => {

        RakshakAI.init();

        RakshakAI.start();

    }

);

/* =====================================================
   GLOBAL DEBUG ACCESS
===================================================== */

window.RakshakAI = RakshakAI;

/* =====================================================
   END OF FILE
===================================================== */
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("qrImage");
const preview = document.getElementById("preview");
const form = document.getElementById("qrForm");
const scanButton = document.getElementById("scanButton");

let selectedFile = null;

// -----------------------------------------------------
// File Selection
// -----------------------------------------------------

dropZone.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", (e) => {

    if (!e.target.files.length) return;

    selectedFile = e.target.files[0];

    showPreview(selectedFile);

});

// -----------------------------------------------------
// Drag & Drop
// -----------------------------------------------------

dropZone.addEventListener("dragover", (e) => {

    e.preventDefault();

    dropZone.classList.add(
        "border-cyan-300",
        "bg-slate-800"
    );

});

dropZone.addEventListener("dragleave", () => {

    dropZone.classList.remove(
        "border-cyan-300",
        "bg-slate-800"
    );

});

dropZone.addEventListener("drop", (e) => {

    e.preventDefault();

    dropZone.classList.remove(
        "border-cyan-300",
        "bg-slate-800"
    );

    if (!e.dataTransfer.files.length)
        return;

    selectedFile = e.dataTransfer.files[0];

    showPreview(selectedFile);

});

// -----------------------------------------------------
// Preview
// -----------------------------------------------------

function showPreview(file) {

    const reader = new FileReader();

    reader.onload = function (event) {

        preview.src = event.target.result;

        preview.classList.remove("hidden");

    };

    reader.readAsDataURL(file);

}

// -----------------------------------------------------
// Upload
// -----------------------------------------------------

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    if (!selectedFile) {

        alert("Please select a QR image.");

        return;

    }

    scanButton.disabled = true;

    scanButton.innerHTML = `
        <svg class="animate-spin h-5 w-5 inline mr-2"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24">

            <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4">
            </circle>

            <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8H4z">
            </path>

        </svg>

        Scanning...
    `;

    const formData = new FormData();

    formData.append("file", selectedFile);

    try {

        const response = await fetch("/api/qr", {

            method: "POST",

            body: formData

        });

        const result = await response.json();

        if (!result.success) {

            alert(result.message || "Analysis failed.");

            resetButton();

            return;

        }

        sessionStorage.setItem(
            "qrResult",
            JSON.stringify(result)
        );

        window.location.href = "/qr/result";

    }

    catch (error) {

        console.error(error);

        alert("Server connection failed.");

    }

    finally {

        resetButton();

    }

});

// -----------------------------------------------------
// Reset Button
// -----------------------------------------------------

function resetButton() {

    scanButton.disabled = false;

    scanButton.innerHTML = "Analyze QR Code";

}
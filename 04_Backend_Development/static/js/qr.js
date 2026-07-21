const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("qrImage");
const preview = document.getElementById("preview");
const form = document.getElementById("qrForm");
const scanButton = document.getElementById("scanButton");
const clearBtn = document.getElementById("clearBtn");


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
// Clear Workspace
// -----------------------------------------------------

function clearWorkspace() {

    selectedFile = null;

    fileInput.value = "";

    preview.src = "";

    preview.classList.add("hidden");

}

clearBtn.addEventListener("click", () => {

    clearWorkspace();

});

// -----------------------------------------------------
// AI Loading Animation
// -----------------------------------------------------

const loadingSteps = [

    "Reading QR Image...",

    "Decoding QR Pattern...",

    "Extracting Embedded Content...",

    "Running AI Detection Models...",

    "Checking URL Reputation...",

    "Analyzing Threat Indicators...",

    "Generating Investigation Report..."

];

let loadingInterval = null;

function startLoading() {

    let index = 0;

    scanButton.disabled = true;

    scanButton.innerHTML = loadingSteps[0];

    loadingInterval = setInterval(() => {

        index++;

        if (index >= loadingSteps.length) {

            index = loadingSteps.length - 1;

        }

        scanButton.innerHTML = loadingSteps[index];

    }, 700);

}

function stopLoading() {

    clearInterval(loadingInterval);

    scanButton.disabled = false;

    scanButton.innerHTML = "Analyze QR";

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

    startLoading();
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

            stopLoading();

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

        stopLoading();

    }

    finally {

        stopLoading();

    }

});

// -----------------------------------------------------
// Reset Button
// -----------------------------------------------------

function resetButton() {

    scanButton.disabled = false;

    scanButton.innerHTML = "Analyze QR Code";

}
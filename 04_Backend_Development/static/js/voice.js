document
    .getElementById("voiceForm")
    .addEventListener("submit", async function (e) {

        e.preventDefault();

        const formData = new FormData();

        formData.append(
            "audio",
            document.getElementById("audio").files[0]
        );

        const response = await fetch("/api/voice", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        sessionStorage.setItem(
            "voice_result",
            JSON.stringify(data)
        );

        window.location.href = "/voice-result";

    });
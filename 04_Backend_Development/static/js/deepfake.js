document
    .getElementById("deepfakeForm")
    .addEventListener("submit", async function (e) {

        e.preventDefault();

        const file = document.getElementById("image").files[0];

        if (!file) {
            alert("Please select an image.");
            return;
        }

        const formData = new FormData();
        formData.append("image", file);

        try {

            const response = await fetch("/api/deepfake", {
                method: "POST",
                body: formData,
            });

            const text = await response.text();

            console.log("Raw Response:", text);

            let data;

            try {
                data = JSON.parse(text);
            } catch (e) {
                alert(text);
                return;
            }

            console.log("Deepfake API Response:", data);

            if (!response.ok || !data.success) {

                alert(
                    data.error ||
                    data.message ||
                    "Deepfake analysis failed."
                );

                return;
            }

            sessionStorage.setItem(
                "deepfake_result",
                JSON.stringify(data)
            );

            window.location.href = "/deepfake-result";

        }
        catch (err) {

            console.error(err);

            alert("Unable to connect to the server.");

        }

    });
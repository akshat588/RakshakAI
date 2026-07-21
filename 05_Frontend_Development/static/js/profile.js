document.addEventListener("DOMContentLoaded", async () => {

    const profileInfo = document.getElementById("profileInfo");
    const preferencesInfo = document.getElementById("preferencesInfo");
    const apiKeys = document.getElementById("apiKeys");

    async function loadProfile() {

        try {

            const response = await fetch("/api/profile");

            const data = await response.json();

            if (!data.success) {

                profileInfo.innerHTML = "Unable to load profile.";
                preferencesInfo.innerHTML = "";
                apiKeys.innerHTML = "";

                return;
            }

            const profile = data.profile;
            const preferences = data.preferences || {};
            const keys = data.api_keys || [];

            profileInfo.innerHTML = `
                <p><strong>Name:</strong> ${profile.name}</p>
                <p><strong>Email:</strong> ${profile.email}</p>
                <p><strong>Role:</strong> ${profile.role}</p>
                <p><strong>Joined:</strong> ${profile.created_at}</p>
            `;

            preferencesInfo.innerHTML = `
                <p><strong>Language:</strong> ${preferences.language || "English"}</p>
                <p><strong>Theme:</strong> ${preferences.theme || "Default"}</p>
                <p><strong>Notifications:</strong> ${preferences.notifications ? "Enabled" : "Disabled"}</p>
            `;

            if (!keys.length) {

                apiKeys.innerHTML = "<p>No API Keys available.</p>";

            } else {

                apiKeys.innerHTML = keys.map(key => `
                    <div class="card mb-3">
                        <p><strong>Name:</strong> ${key.name}</p>
                        <p><strong>Key:</strong> ${key.masked_key}</p>
                        <p><strong>Status:</strong> ${key.status}</p>
                    </div>
                `).join("");

            }

        } catch (error) {

            profileInfo.innerHTML = error.message;

        }

    }

    loadProfile();

});
document.addEventListener("DOMContentLoaded", () => {

    console.log("RakshakAI Frontend Initialized");

    // Initialize Lucide Icons
    lucide.createIcons();

    // Hide Loader
    window.addEventListener("load", () => {

        setTimeout(() => {

            const loader = document.getElementById("loader");

            if (loader) {

                loader.style.opacity = "0";

                setTimeout(() => {

                    loader.remove();

                }, 400);

            }

        }, 700);

    });

});
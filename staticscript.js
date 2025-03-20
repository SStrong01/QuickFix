document.addEventListener("DOMContentLoaded", function () {
    const generateButton = document.getElementById("generate-btn");
    const buyNowButton = document.getElementById("buy-now-btn");
    const ideasContainer = document.getElementById("ideas-container");

    generateButton.addEventListener("click", async function () {
        const niche = document.getElementById("niche").value;
        const platform = document.getElementById("platform").value;

        if (!niche || !platform) {
            alert("Please enter a niche and select a platform.");
            return;
        }

        try {
            const response = await fetch("/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ niche, platform }),
            });

            const data = await response.json();

            if (data.error) {
                alert("Error: " + data.error);
                return;
            }

            sessionStorage.setItem("ideas", JSON.stringify(data.ideas));

            ideasContainer.innerHTML = "<h3>Your AI-Generated Ideas:</h3><ul>" +
                data.ideas.map(idea => `<li>${idea}</li>`).join("") + "</ul>";

        } catch (error) {
            alert("An error occurred while generating ideas.");
        }
    });

    buyNowButton.addEventListener("click", async function () {
        try {
            const response = await fetch("/checkout", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            });

            const data = await response.json();

            if (data.error) {
                alert("Payment error: " + data.error);
                return;
            }

            window.location.href = data.checkout_url;

        } catch (error) {
            alert("An error occurred during checkout.");
        }
    });

    if (window.location.pathname === "/success") {
        const storedIdeas = sessionStorage.getItem("ideas");
        if (storedIdeas) {
            ideasContainer.innerHTML = "<h3>Your AI-Generated Ideas:</h3><ul>" +
                JSON.parse(storedIdeas).map(idea => `<li>${idea}</li>`).join("") + "</ul>";
        } else {
            ideasContainer.innerHTML = "<p>No ideas found. Please generate new ones.</p>";
        }
    }
});
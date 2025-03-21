document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded successfully!");

    // Select elements
    const buyButton = document.getElementById("buyNowButton");
    const generateButton = document.getElementById("generateIdeas");
    const ideasContainer = document.getElementById("ideasContainer");
    const nicheInput = document.getElementById("niche");
    const platformSelect = document.getElementById("platform");

    // ✅ Buy Now Button Click Event
    if (buyButton) {
        buyButton.addEventListener("click", function () {
            console.log("Buy Now button clicked!");
            fetch("/create-checkout-session", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.url) {
                    window.location.href = data.url; // Redirect to Stripe Checkout
                } else {
                    alert("Error: Could not process payment.");
                }
            })
            .catch(error => console.error("Error:", error));
        });
    } else {
        console.error("Buy Now button not found!");
    }

    // ✅ Generate Ideas Button Click Event
    if (generateButton) {
        generateButton.addEventListener("click", function () {
            const niche = nicheInput.value.trim();
            const platform = platformSelect.value.trim();

            if (!niche || !platform) {
                alert("Please enter a niche and select a platform.");
                return;
            }

            console.log("Generating ideas for:", niche, platform);

            fetch("/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ niche: niche, platform: platform }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(`Error: ${data.error}`);
                    return;
                }

                ideasContainer.innerHTML = ""; // Clear previous ideas
                data.ideas.forEach((idea, index) => {
                    const ideaElement = document.createElement("p");
                    ideaElement.innerHTML = `🔥 <strong>${index + 1}. ${idea}</strong>`;
                    ideasContainer.appendChild(ideaElement);
                });
            })
            .catch(error => console.error("Error:", error));
        });
    } else {
        console.error("Generate Ideas button not found!");
    }
});

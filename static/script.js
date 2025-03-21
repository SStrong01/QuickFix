document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded successfully!");

    // Select elements
    const buyButton = document.getElementById("buyNowButton");
    const generateButton = document.getElementById("generateIdeas");
    const ideasContainer = document.getElementById("ideasContainer");
    const nicheInput = document.getElementById("niche");
    const platformSelect = document.getElementById("platform");

    // ✅ Ensure the "Buy Now" button works
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
                    alert("Payment processing failed.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error processing payment. Check console for details.");
            });
        });
    } else {
        console.error("Buy Now button not found!");
    }

    // ✅ Ensure the "Generate Ideas" button works
    if (generateButton) {
        generateButton.addEventListener("click", function () {
            const niche = nicheInput.value.trim();
            const platform = platformSelect.value.trim();

            if (!niche || !platform) {
                alert("Please enter a niche and select a platform.");
                return;
            }

            console.log(`Requesting AI-generated ideas for: ${niche} on ${platform}`);

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

                ideasContainer.innerHTML = ""; // Clear old ideas
                if (data.ideas.length === 0) {
                    ideasContainer.innerHTML = "<p>No ideas found. Try another niche.</p>";
                } else {
                    data.ideas.forEach((idea, index) => {
                        const ideaElement = document.createElement("p");
                        ideaElement.innerHTML = `🔥 <strong>${index + 1}. ${idea}</strong>`;
                        ideasContainer.appendChild(ideaElement);
                    });
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error fetching AI ideas. Check console for details.");
            });
        });
    } else {
        console.error("Generate Ideas button not found!");
    }
});

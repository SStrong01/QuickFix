document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded successfully!");

    // Select buttons
    const buyNowButton = document.getElementById("buyNow");
    const generateIdeasButton = document.getElementById("generateIdeas");

    if (!buyNowButton) {
        console.error("❌ Buy Now button not found!");
    } else {
        console.log("✅ Buy Now button found!");
    }

    if (!generateIdeasButton) {
        console.error("❌ Generate Ideas button not found!");
    } else {
        console.log("✅ Generate Ideas button found!");
    }

    // Handle Buy Now Button Click
    if (buyNowButton) {
        buyNowButton.addEventListener("click", function () {
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
                    window.location.href = data.url; // Redirect to Stripe checkout
                } else {
                    console.error("❌ Stripe URL not received!");
                    alert("Payment failed. Please try again.");
                }
            })
            .catch(error => {
                console.error("❌ Error processing payment:", error);
                alert("An error occurred. Please try again.");
            });
        });
    }

    // Handle Generate Ideas Button Click
    if (generateIdeasButton) {
        generateIdeasButton.addEventListener("click", function () {
            console.log("Generate Ideas button clicked!");

            const niche = document.getElementById("niche").value;
            const platform = document.getElementById("platform").value;

            if (!niche || !platform) {
                alert("Please enter a niche and select a platform.");
                return;
            }

            fetch("/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ niche, platform }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.ideas) {
                    console.log("✅ AI Ideas generated:", data.ideas);

                    const ideasList = document.getElementById("ideasList");
                    ideasList.innerHTML = ""; // Clear previous ideas

                    data.ideas.forEach((idea, index) => {
                        const listItem = document.createElement("li");
                        listItem.textContent = `🔥 ${idea}`;
                        ideasList.appendChild(listItem);
                    });
                } else {
                    console.error("❌ No ideas received from the server.");
                    alert("Failed to generate ideas. Please try again.");
                }
            })
            .catch(error => {
                console.error("❌ Error fetching AI ideas:", error);
                alert("An error occurred. Please try again.");
            });
        });
    }
});

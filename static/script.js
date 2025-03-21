document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded Successfully");

    // Handle "Buy Now" button click
    let buyButton = document.getElementById("buy-button"); // Ensure the button has this ID

    if (buyButton) {
        buyButton.addEventListener("click", function () {
            console.log("Buy Button Clicked!");
            alert("Redirecting to payment...");
            window.location.href = "/checkout"; // Update with your actual payment URL
        });
    } else {
        console.error("Buy button not found!");
    }

    // Handle AI idea generation
    let generateButton = document.getElementById("generate-ideas");

    if (generateButton) {
        generateButton.addEventListener("click", function () {
            console.log("Generating AI Ideas...");
            let niche = document.getElementById("niche").value;
            let platform = document.getElementById("platform").value;

            if (!niche || !platform) {
                alert("Please enter a niche and select a platform.");
                return;
            }

            fetch("/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ niche: niche, platform: platform })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Generated Ideas:", data);
                let ideaList = document.getElementById("idea-list");
                ideaList.innerHTML = ""; // Clear previous ideas

                if (data.ideas && data.ideas.length > 0) {
                    data.ideas.forEach(idea => {
                        let li = document.createElement("li");
                        li.textContent = idea;
                        ideaList.appendChild(li);
                    });
                } else {
                    ideaList.innerHTML = "<li>No ideas found. Please try again.</li>";
                }
            })
            .catch(error => {
                console.error("Error fetching AI ideas:", error);
                alert("Error generating ideas. Please try again.");
            });
        });
    } else {
        console.error("Generate button not found!");
    }
});
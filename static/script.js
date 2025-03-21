document.addEventListener("DOMContentLoaded", function() {
    const generateButton = document.getElementById("generate-button");
    const buyNowButton = document.getElementById("buy-now");
    const ideasContainer = document.getElementById("ideas-container");

    generateButton.addEventListener("click", function() {
        const niche = document.getElementById("niche").value;
        const platform = document.getElementById("platform").value;

        if (!niche) {
            alert("Please enter a niche!");
            return;
        }

        fetch('/generate', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ niche: niche, platform: platform })
        })
        .then(response => response.json())
        .then(data => {
            ideasContainer.innerHTML = ""; // Clear previous ideas
            if (data.ideas) {
                data.ideas.forEach(idea => {
                    const li = document.createElement("li");
                    li.textContent = idea;
                    ideasContainer.appendChild(li);
                });
            } else {
                ideasContainer.innerHTML = "<li>No ideas found. Please try again.</li>";
            }
        })
        .catch(error => console.error("Error:", error));
    });

    buyNowButton.addEventListener("click", function() {
        fetch('/checkout', { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.checkout_url) {
                window.location.href = data.checkout_url;
            } else {
                alert("Error: " + (data.error || "Payment failed"));
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
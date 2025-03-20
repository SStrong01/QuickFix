document.getElementById("generate-button").addEventListener("click", () => {
    const niche = document.getElementById("niche").value;
    const platform = document.getElementById("platform").value;

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ niche, platform })
    })
    .then(response => response.json())
    .then(data => {
        if (data.ideas) {
            localStorage.setItem("ideas", JSON.stringify(data.ideas));
            displayIdeas(data.ideas);
        } else {
            alert("Error generating ideas.");
        }
    })
    .catch(error => console.error("Error:", error));
});

document.getElementById("buy-now").addEventListener("click", () => {
    fetch("/checkout", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        if (data.url) {
            window.location.href = data.url;
        } else {
            alert("Payment failed.");
        }
    })
    .catch(error => console.error("Checkout error:", error));
});

function displayIdeas(ideas) {
    const container = document.getElementById("ideas-container");
    container.innerHTML = ideas.map(idea => `<li>${idea}</li>`).join("");
}

window.onload = () => {
    const savedIdeas = JSON.parse(localStorage.getItem("ideas"));
    if (savedIdeas) displayIdeas(savedIdeas);
};

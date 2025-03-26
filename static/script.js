document.addEventListener("DOMContentLoaded", function () {
  const generateButton = document.getElementById("generate-button");
  const buyNowButton = document.getElementById("buy-now");
  const ideasContainer = document.getElementById("ideas-container");

  generateButton.addEventListener("click", async function () {
    const niche = document.getElementById("niche").value.trim();
    const platform = document.getElementById("platform").value;

    if (!niche) {
      alert("Please enter a niche.");
      return;
    }

    try {
      const response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ niche, platform })
      });

      const data = await response.json();
      ideasContainer.innerHTML = "";

      if (data.ideas && data.ideas.length > 0) {
        data.ideas.forEach(idea => {
          const li = document.createElement("li");
          li.textContent = idea;
          ideasContainer.appendChild(li);
        });
      } else {
        ideasContainer.innerHTML = "<li>No ideas found. Try again.</li>";
      }
    } catch (error) {
      console.error("Error generating ideas:", error);
      ideasContainer.innerHTML = "<li>Something went wrong. Try again later.</li>";
    }
  });

  buyNowButton.addEventListener("click", async function () {
    try {
      const response = await fetch("/checkout", {
        method: "POST"
      });

      const data = await response.json();

      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        alert("Payment failed: " + (data.error || "Unknown error"));
      }
    } catch (error) {
      console.error("Payment error:", error);
      alert("Something went wrong during payment.");
    }
  });
});
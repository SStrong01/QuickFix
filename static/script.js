document.addEventListener("DOMContentLoaded", function () {
  const buyButton = document.getElementById("buy-now");

  buyButton.addEventListener("click", function () {
    const niche = document.getElementById("niche").value;
    const platform = document.getElementById("platform").value;

    fetch("/checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ niche: niche, platform: platform })
    })
    .then(res => res.json())
    .then(data => {
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        alert("Payment failed or server error.");
      }
    })
    .catch(err => console.error("Checkout Error:", err));
  });
});

document.addEventListener("DOMContentLoaded", function () {
    const generateBtn = document.getElementById("generate-button");
    const buyNowBtn = document.getElementById("buy-now");

    let ideasGenerated = false;

    generateBtn.addEventListener("click", function () {
        const niche = document.getElementById("niche").value;
        const platform = document.getElementById("platform").value;

        if (!niche || !platform) {
            alert("Please enter a niche and platform.");
            return;
        }

        fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ niche, platform })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Ideas generated! Now click 'Buy Now' to unlock them.");
                ideasGenerated = true;
            } else {
                alert("Error generating ideas: " + data.error);
            }
        })
        .catch(err => {
            console.error(err);
            alert("Something went wrong.");
        });
    });

    buyNowBtn.addEventListener("click", function () {
        if (!ideasGenerated) {
            alert("Please generate ideas before purchasing.");
            return;
        }

        fetch("/checkout", {
            method: "POST"
        })
        .then(res => res.json())
        .then(data => {
            if (data.checkout_url) {
                window.location.href = data.checkout_url;
            } else {
                alert("Checkout failed: " + data.error);
            }
        })
        .catch(err => {
            console.error(err);
            alert("Something went wrong during checkout.");
        });
    });
});
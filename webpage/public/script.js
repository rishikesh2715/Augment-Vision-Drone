document
  .getElementById("subscribe-button")
  .addEventListener("click", function () {
    const email = document.getElementById("newsletter-email").value;

    // Perform client-side validation here (e.g., check for a valid email format)
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    if (!emailRegex.test(email)) {
      alert("Invalid email format");
      return; // Exit the function early
    }

    // Send the email to the server for further processing
    fetch("/subscribe", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email }),
    })
      .then((response) => {
        if (response.ok) {
          // Display a success message to the user
          alert("Subscription successful! Check your email for confirmation.");
          document.getElementById("newsletter-email").value = "";
        } else {
          // Parse the JSON error response and display the error message
          response
            .json()
            .then((data) => {
              alert(`Subscription failed. ${data.error}`);
            })
            .catch((error) => {
              console.error("Error parsing JSON response:", error);
              alert("Subscription failed. An error occurred.");
            });
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

document
  .getElementById("loginForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      credentials: "include", // ✅ tells browser to store the cookie
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
      }),
    });

    const data = await response.json();
    if (response.ok) {
      alert("Login successful");
      // Redirect to a protected page if needed
    } else {
      alert(data.detail || "Login failed");
    }
  });

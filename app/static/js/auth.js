async function refreshToken() {
  try {
    const res = await fetch("/auth/refresh", {
      method: "POST",
      credentials: "include",
    });
    if (!res.ok) window.location.href = "/auth/login";
  } catch (err) {
    console.error("Refresh token error", err);
    window.location.href = "/auth/login";
  }
}

setInterval(refreshToken, 1 * 60 * 1000); // Every 10 minutes

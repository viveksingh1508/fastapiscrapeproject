document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("job-search-form");
  const warning = document.getElementById("search-warning");

  form.addEventListener("submit", function (e) {
    const keyword = form.keyword.value.trim();
    const location = form.location.value.trim();
    const path = window.location.pathname;

    // const existing = document.getElementById("search-warning");
    // if (existing) existing.remove();

    if (!keyword && !location) {
      e.preventDefault();

      if (path === "/") {
        // Show warning on home page
        warning.textContent = "Please enter a keyword or location to search.";
        warning.style.display = "block";
      } else if (path.startsWith("/jobs")) {
        // Redirect to home from jobs page
        window.location.href = "/";
      }
    }
  });
});

function togglePassword(fieldId, toggleElement) {
  const passwordField = document.getElementById(fieldId);
  const isHidden = passwordField.type === "password";

  passwordField.type = isHidden ? "text" : "password";
  toggleElement.textContent = isHidden ? "Hide" : "Show";
}

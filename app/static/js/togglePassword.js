function togglePassword(fieldId) {
  const passwordField = document.getElementById(fieldId);
  passwordField.type = passwordField.type === "password" ? "text" : "password";
}

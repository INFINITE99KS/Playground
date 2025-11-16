const loginForm = document.querySelector("#login");
const registerForm = document.querySelector("#register");
const formContainer = document.querySelector(".form-container");

const loginBtn = document.querySelector("#loginBtn");
const registerBtn = document.querySelector("#registerBtn");

// initialize
loginForm.classList.add("hidden");
registerForm.classList.add("hidden");
formContainer.style.height = "0px";

// make sure buttons toggle style correctly
function setActive(active) {
  if (active === "login") {
    loginBtn.classList.add("btn-primary");
    loginBtn.classList.remove("btn-outline-primary");

    registerBtn.classList.add("btn-outline-primary");
    registerBtn.classList.remove("btn-primary");
  } else {
    registerBtn.classList.add("btn-primary");
    registerBtn.classList.remove("btn-outline-primary");

    loginBtn.classList.add("btn-outline-primary");
    loginBtn.classList.remove("btn-primary");
  }
}

function showLogin() {
  registerForm.classList.add("hidden");
  loginForm.classList.remove("hidden");
  formContainer.style.height = loginForm.scrollHeight + "px";
  setActive("login");
}

function showRegister() {
  loginForm.classList.add("hidden");
  registerForm.classList.remove("hidden");
  formContainer.style.height = registerForm.scrollHeight + "px";
  setActive("register");
}

const username = document.getElementById('username');
const password = document.getElementById('password');
const confirmation = document.getElementById('confirmation');
const submitBtn = document.getElementById('submitBtn')
function validateForm() {
    const userValid = username.value.trim() !== '';
    const passwordsMatch = password.value === confirmation.value && password.value !== '';
    submitBtn.disabled = !(userValid && passwordsMatch);
}
username.addEventListener('input', validateForm);
password.addEventListener('input', validateForm);
confirmation.addEventListener('input', validateForm);


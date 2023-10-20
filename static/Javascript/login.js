function signup() {
    document.querySelector(".login-form-container").style.display = "none";
    document.querySelector(".signup-form-container").style.display = "block";
    document.querySelector(".container").style.background = "linear-gradient(to bottom, rgb(242, 36, 36),  rgb(252, 207, 25))";
    document.querySelector(".button-1").style.display = "none";
    document.querySelector(".button-2").style.display = "block";
    document.querySelector(".content-holder h4").textContent = "Have an account?";
}

function login() {
    document.querySelector(".signup-form-container").style.display = "none";
    document.querySelector(".login-form-container").style.display = "block";
    document.querySelector(".container").style.background = "linear-gradient(to bottom, rgb(252, 207, 25),  rgb(242, 36, 36))";
    document.querySelector(".button-2").style.display = "none";
    document.querySelector(".button-1").style.display = "block";
    document.querySelector(".content-holder h4").textContent = "Don't have an account?";
}

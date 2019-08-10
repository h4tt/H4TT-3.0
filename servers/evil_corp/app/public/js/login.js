window.onload = () => {
    const errorDiv = document.getElementById("error");
    const urlParams = new URLSearchParams(window.location.search);
    const badAuth = urlParams.get("badauth");

    if (badAuth == "true") {
        errorDiv.style.opacity = 1;
        setTimeout(() => {
            errorDiv.style.opacity = 0;
        }, 3000);
    }
};

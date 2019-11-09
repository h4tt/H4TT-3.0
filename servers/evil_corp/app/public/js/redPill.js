window.onload = () => {
    const response = document.getElementById("response");
    const form = document.getElementById("request-pill");
    const token = document.getElementById("token");

    form.addEventListener("submit", e => {
        e.preventDefault();
        let xhr = new XMLHttpRequest();
        xhr.open("POST", "/the-red-pill");
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onerror = () => {
            setResponse("Something went wrong with the client.");
        };

        xhr.onload = () => {
            setResponse(JSON.parse(xhr.response)["response"]);
        };

        xhr.send(JSON.stringify({ token: token.value }));
    });

    function setResponse(text) {
        response.innerHTML = text;
    }
};

let socket = null;

const button = document.getElementById("connectButton");
const status = document.getElementById("status");

button.addEventListener("click", () => {

    socket = new WebSocket("ws://localhost:8765");

    socket.onopen = () => {

        status.textContent = "Connected";

        socket.send(JSON.stringify({
            type: "join",
            name: "Player"
        }));

    };

    socket.onclose = () => {
        status.textContent = "Disconnected";
    };

    socket.onmessage = (event) => {

    const data = JSON.parse(event.data);

    if (data.type === "status") {

        status.textContent = data.message;

    }

    if (data.type === "start") {

        status.textContent = "GO!";

        document.getElementById("text").textContent = data.text;

    }

};

});
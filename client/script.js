let socket = null;

const textDiv = document.getElementById("text"); 

let targetText = "";
let started = false;
let startTime = 0;
let mistakes = 0;

const button = document.getElementById("connectButton");
const status = document.getElementById("status");
const input = document.getElementById("typingInput");
input.disabled = true;
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

    switch (data.type) {

        case "status":
            status.textContent = data.message;
            break;

        case "countdown":
            document.getElementById("text").textContent = "";
            status.textContent = data.value;
            break;

        case "start":
            input.disabled = false;

            input.focus();

            input.value = "";

            status.textContent = "GO!";

            targetText = data.text;

            renderText("");

            started = false;

            mistakes = 0;

            break;
    }

};

});

function renderText(userInput) {

    let html = "";

    for (let i = 0; i < targetText.length; i++) {

        if (i < userInput.length) {

            if (userInput[i] === targetText[i]) {

                html += `<span class="correct">${targetText[i]}</span>`;

            } else {

                html += `<span class="incorrect">${targetText[i]}</span>`;

            }

        }

        else if (i === userInput.length) {

            html += `<span class="current">${targetText[i]}</span>`;

        }

        else {

            html += targetText[i];

        }

    }

    textDiv.innerHTML = html;

}

input.addEventListener("input", ()=>{
    if(!started){
        started = true;
        startTime = Date.now();
    }

    renderText(input.value);

    updateStats();

    if(input.value===targetText){
        finishRound();
    }
});

function updateStats(){
    const typed = input.value.length;
    let correct = 0;
    mistakes = 0;
    for(let i=0; i<typed; i++){
        if(input.value[i]===targetText[i]){
            correct++;
        }
        else{
            mistakes++;
        }
    }
    const accuracy = 
        typed === 0 
            ? 100
            : (correct/typed)*100;
    const elapsed = (Date.now()-startTime)/60000;
    let wpm = 0;
    if(started&&elapsed>0){
        wpm = (typed/5)/elapsed;
    }
    document.getElementById("wpm").textContent = `WPM: ${Math.round(wpm)}`;
    document.getElementById("accuracy").textContent = `Accuracy: ${accuracy.toFixed(1)}%`;
}

function finishRound(){
    input.disabled = true;
    const elapsed = (Date.now() - startTime)/1000;
    socket.send(JSON.stringify({
        type : "finished",
        time : elapsed,
        mistakes : mistakes
    }));
}
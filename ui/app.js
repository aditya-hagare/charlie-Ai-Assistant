// ================= CONFIG =================
const API_BASE = "http://127.0.0.1:8000";


// ================= BROWSER SPEECH RECOGNITION =================

let recognition;

if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-IN"; // change if needed
} else {
    console.log("Speech Recognition not supported in this browser.");
}


// ================= THREE SETUP =================
const canvas = document.getElementById("globe");
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(70, 1, 0.1, 1000);
camera.position.z = 2.2;

const renderer = new THREE.WebGLRenderer({ canvas, alpha: true });
renderer.setSize(canvas.clientWidth, canvas.clientHeight);

// ================= GLOBE =================
const sphere = new THREE.Mesh(
    new THREE.SphereGeometry(0.6, 64, 64),
    new THREE.MeshBasicMaterial({
        color: 0x00ffaa,
        wireframe: true,
        transparent: true,
        opacity: 0.5
    })
);
scene.add(sphere);


// ================= AUDIO VISUALIZER =================
let analyser, dataArray;

async function setupMic() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const ctx = new AudioContext();
    const src = ctx.createMediaStreamSource(stream);
    analyser = ctx.createAnalyser();
    analyser.fftSize = 256;
    src.connect(analyser);
    dataArray = new Uint8Array(analyser.frequencyBinCount);
}

// ================= UI STATE =================
const statusText = document.getElementById("status-text");

function setState(s) {
    statusText.innerText =
        s === "thinking" ? "ANALYZING" :
        s === "speaking" ? "RESPONDING" :
        "CHARLIE READY";
}

// ================= ANIMATION =================
function animate() {
    requestAnimationFrame(animate);

    if (analyser) {
        analyser.getByteFrequencyData(dataArray);
        bars.forEach((bar, i) => {
            const v = dataArray[i] / 255;
            bar.scale.y = 0.5 + v * 2;
        });
    }

    sphere.rotation.y += 0.002;
    renderer.render(scene, camera);
}
animate();

// ================= CHAT SYSTEM =================
function addMessage(text, sender) {
    const container = document.getElementById("chat-messages");

    const msg = document.createElement("div");
    msg.className = "message " + sender;
    msg.innerText = text;

    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
}

function addHistory(text) {
    const historyBox = document.getElementById("history");
    if (!historyBox) return;

    const item = document.createElement("div");
    item.className = "history-item";
    item.innerText = text;

    // Clicking history sends message again
    item.onclick = () => sendMessage(text);

    historyBox.prepend(item);
}


function sendMessage(textParam = null) {
    const input = document.getElementById("userInput");
    const text = textParam || input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    addHistory(text);
    
    input.value = "";

    const container = document.getElementById("chat-messages");

    const typingDiv = document.createElement("div");
    typingDiv.className = "message ai typing";
    typingDiv.innerHTML = `Charlie is typing <span>.</span><span>.</span><span>.</span>`;
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;

    setState("thinking");

    fetch(`${API_BASE}/command`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    })
    .then(res => res.json())
    .then(data => {
        container.removeChild(typingDiv);
        addMessage(data.response, "ai");
        setState("speaking");
        setTimeout(() => setState("idle"), 1500);
    })
    .catch(() => {
        container.removeChild(typingDiv);
        addMessage("Error connecting to backend.", "ai");
        setState("idle");
    });
}

// Enter key support
document.getElementById("userInput").addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

// Command buttons
document.querySelectorAll(".cmd").forEach(cmd => {
    cmd.onclick = () => sendMessage(cmd.innerText);
});

// ================= LEFT PANEL =================

// WEATHER
async function loadWeather() {
    try {
        const res = await fetch(`${API_BASE}/api/weather?city=Pune`);
        const data = await res.json();

        document.getElementById("weather-text").innerText =
            `${data.temp}°C | Wind ${data.wind} km/h`;
    } catch {
        document.getElementById("weather-text").innerText = "Weather unavailable";
    }
}

// NEWS
async function loadNews() {
    try {
        const res = await fetch(`${API_BASE}/api/news?topic=india`);
        const data = await res.json();

        const list = document.getElementById("news-list");
        list.innerHTML = "";

        if (!data.headlines || data.headlines.length === 0) {
            list.innerHTML = "<li>No news available</li>";
            return;
        }

        data.headlines.forEach(headline => {
            const li = document.createElement("li");
            li.textContent = "• " + headline;
            list.appendChild(li);
        });
    } catch {
        console.error("News error");
    }
}

// STOCKS
async function loadStocks() {
    try {
        const res = await fetch(`${API_BASE}/api/stocks`);
        const data = await res.json();

        const container = document.getElementById("stock-text");

        container.innerHTML = `
            <div>🇮🇳 NIFTY 50: ${data.nifty50?.price ?? "—"}</div>
            <div>₿ BTC/USD: ${data.btcusd?.price ?? "—"}</div>
            <div>🟡 GOLD: ${data.gold?.price ?? "—"}</div>
        `;
    } catch {
        console.error("Stocks error");
    }
}

// Initial Load
loadWeather();
loadNews();
loadStocks();

// Auto Refresh
setInterval(loadWeather, 60000);
setInterval(loadNews, 300000);
setInterval(loadStocks, 60000);


//mic button //

// ================= MIC BUTTON =================

const micBtn = document.getElementById("mic-btn");

micBtn.addEventListener("click", function () {

    micBtn.classList.add("active");

    if (!recognition) {
        alert("Speech recognition not supported.");
        return;
    }

    recognition.start();
});


recognition.onend = function () {
    micBtn.classList.remove("active");
    setState("idle");
};

recognition.onresult = function (event) {

    const transcript = event.results[0][0].transcript.trim();

    console.log("You said:", transcript);

    addMessage(transcript, "user");
    addHistory(transcript);

    fetch(`${API_BASE}/command`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: transcript })
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.response, "ai");
        setState("speaking");
        setTimeout(() => setState("idle"), 1500);
    })
    .catch(() => {
        addMessage("Error connecting to backend.", "ai");
        setState("idle");
    });
};


recognition.onerror = function (event) {
    console.error("Speech recognition error:", event.error);
    setState("idle");
};


//  toogle // TTS TOGGLE

const ttsToggle = document.getElementById("tts-toggle");

ttsToggle.onclick = async () => {
    const res = await fetch("http://127.0.0.1:8000/toggle-tts", {
        method: "POST"
    });

    const data = await res.json();

    if (data.tts_enabled) {
        ttsToggle.innerText = "🔊";
    } else {
        ttsToggle.innerText = "🔇";
    }
};


function minimizeApp() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.minimize();
    } else {
        console.log("API not ready yet");
    }
}

function closeApp() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.hide();
    } else {
        console.log("API not ready yet");
    }
}


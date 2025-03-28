async function sendMessage() {
    const userInput = document.getElementById("userInput");
    const userMessage = userInput.value.trim();  // Remove extra spaces

    if (!userMessage) return;  // Ignore empty input

    // Append user message to chatbox
    document.getElementById("chatbox").innerHTML += `<p class="message user">${userMessage}</p>`;
    // http://127.0.0.1:8000/webhook
    try {
        const response = await fetch("https://dialogflow-customchatbot.onrender.com/webhook", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: userMessage }) // Sending user input as JSON
        });

        const data = await response.json();
        console.log("Response from backend:", data);

        // Append bot response to chatbox
        document.getElementById("chatbox").innerHTML += `<p class="message bot">${data.response}</p>`;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("chatbox").innerHTML += `<p class="message bot">Error: Unable to connect</p>`;
    }

    userInput.value = "";  // Clear input field
}

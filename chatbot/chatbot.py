from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
import random
import webbrowser

# Expanded logic for chatbot responses
def get_bot_response(user_input):
    user_input = user_input.lower()
    responses = {
        "hello": [
            "Hi there! How can I help you today?", 
            "Hello! What brings you here today?", 
            "Hey! How can I assist you?", 
            "Greetings! What can I do for you?"
        ],
        "how are you": [
            "I'm just a program, but I'm functioning perfectly!", 
            "I'm great, thanks for asking! How about you?", 
            "I'm doing well. What about you?", 
            "I'm here to help, so always feeling good!"
        ],
        "your name": [
            "I'm a smart chatbot created to assist you! What's your name?", 
            "I go by SmartBot. And you?", 
            "Call me SmartBot. What's your name?"
        ],
        "bye": [
            "Goodbye! Have a great day!", 
            "Bye! Take care!", 
            "See you soon! Don't forget to come back.", 
            "Bye-bye! Stay awesome!"
        ],
        "what can you do": [
            "I can chat with you, answer simple questions, and make your day better!", 
            "I'm here to assist you with anything I can.", 
            "I can chat, tell jokes, and help you with basic queries."
        ],
        "tell me a joke": [
            "Why don’t skeletons fight each other? They don’t have the guts!", 
            "Why was the math book sad? It had too many problems.", 
            "Why did the scarecrow win an award? Because he was outstanding in his field!", 
            "Why did the bicycle fall over? It was two-tired!"
        ],
        "weather": [
            "I can't provide real-time weather updates yet, but it's always sunny in our conversation!", 
            "Weather updates aren't my thing yet, but I'm working on it!", 
            "Check outside! That's my best guess. 😊"
        ],
        "i": [
            "Tell me more about yourself!", 
            "It's great to know you better!", 
            "That's interesting. What else can you share about yourself?"
        ],
        "hey": [
            "Hey there! What's up?", 
            "Hello! How can I help you?", 
            "Hi! What's on your mind?"
        ],
        "namaste": [
            "Namaste! How can I assist you?", 
            "Namaste! It's great to connect with you!", 
            "Namaste! How's your day going?"
        ],
        "namaskara": [
            "Namaskara! What can I do for you?", 
            "Namaskara! How's your day going?", 
            "Namaskara! Nice to see you!"
        ],
        "good morning": [
            "Good morning! Hope you have a fantastic day ahead!", 
            "Morning! What's on your mind today?", 
            "Good morning! How can I assist you today?"
        ],
        "good night": [
            "Good night! Sleep well and sweet dreams!", 
            "Nighty night! See you tomorrow.", 
            "Good night! Don't let the bugs bite. 😉"
        ],
        "love": [
            "Love makes the world go round! ❤️", 
            "Love is a beautiful thing. Spread it everywhere!", 
            "Tell me more about what you love!"
        ],
    }

    for key, value in responses.items():
        if key in user_input:
            return random.choice(value)

    return random.choice([
        "I'm not sure how to respond to that. Could you rephrase?", 
        "Hmm, I didn't understand that. Could you try asking differently?", 
        "That's an interesting question! Tell me more.",
        "I'm here to learn more and help. Could you elaborate?"
    ])

# HTML and CSS for the chatbot UI
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Chatbot</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(to bottom, #FF7E5F, #FEB47B);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        #main-container {
            width: 70%;
            height: 80%;
            display: flex;
            flex-direction: column;
            background-color: #1A202C;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }
        #chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            padding: 10px;
            overflow-y: auto;
            scroll-behavior: smooth;
            background-color: #2D3748;
        }
        .message {
            margin: 5px 0;
            max-width: 70%;
            padding: 10px;
            border-radius: 10px;
            animation: fadeIn 0.3s ease;
        }
        .user {
            align-self: flex-end;
            background-color: #38B2AC;
            color: white;
        }
        .bot {
            align-self: flex-start;
            background-color: #4A5568;
            color: white;
        }
        #input-container {
            display: flex;
            gap: 10px;
            padding: 10px;
            background-color: #1A202C;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
        }
        #user-input {
            flex: 1;
            padding: 10px;
            font-size: 16px;
            border: none;
            border-radius: 20px;
            outline: none;
            background-color: #2D3748;
            color: white;
        }
        #send-btn, #upload-btn {
            padding: 10px 20px;
            background-color: #38B2AC;
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            transition: transform 0.5s ease, background-color 0.5s ease, box-shadow 0.5s ease;
        }
        #send-btn:hover, #upload-btn:hover {
            background-color: #319795;
            transform: translateY(-5px) scale(1.1);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
        }
        #upload-btn {
            background-color: #4A5568;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
</head>
<body>
    <div id="main-container">
        <div id="chat-container"></div>
        <div id="input-container">
            <input type="text" id="user-input" placeholder="Type a message...">
            <button id="send-btn">Send</button>
            <input type="file" id="upload-btn" accept="image/*">
        </div>
    </div>
    <script>
        const chatContainer = document.getElementById('chat-container');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');
        const uploadBtn = document.getElementById('upload-btn');

        sendBtn.addEventListener('click', () => {
            const userText = userInput.value.trim();
            if (!userText) return;

            addMessage(userText, 'user');

            fetch(`/chat?input=${encodeURIComponent(userText)}`)
                .then(response => response.json())
                .then(data => {
                    addMessage(data.response, 'bot');
                });

            userInput.value = '';
        });

        uploadBtn.addEventListener('change', () => {
            const file = uploadBtn.files[0];
            if (file) {
                addMessage("Image uploaded!", "user");
                addMessage("Nice image!", "bot");
            }
        });

        function addMessage(text, sender) {
            const message = document.createElement('div');
            message.className = `message ${sender}`;
            message.textContent = text;
            chatContainer.appendChild(message);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    </script>
</body>
</html>
"""

# HTTP server for handling requests
class ChatbotServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/chat"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            user_input = params.get("input", [""])[0]
            response = get_bot_response(user_input)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"response": response}).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))

# Start the chatbot server
if __name__ == "__main__":
    host = "localhost"
    port = 8080
    server = HTTPServer((host, port), ChatbotServer)
    print(f"Chatbot running at http://{host}:{port}")
    webbrowser.open(f"http://{host}:{port}")
    server.serve_forever()

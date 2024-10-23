import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set up Azure OpenAI API credentials
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"  # Replace with the correct version
openai.api_base = "https://vinilhackproject.openai.azure.com/"  # Replace with your endpoint
openai.api_key = "10e4b0dd49924450b87d56aab5e4fc58"  # Replace with your API key

# Function to scrape SC24 program data
def scrape_sc24_programs():
    url = 'https://sc24.supercomputing.org/program/'
    response = requests.get(url)
    programs = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find relevant data; this part depends on the actual HTML structure of the page
        for program in soup.find_all('div', class_='program-details'):
            title = program.find('h3').get_text(strip=True)
            description = program.find('p').get_text(strip=True)
            programs.append({"title": title, "description": description})
    return programs

# Chatbot route to handle user requests
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'response': 'Please provide a message.'}), 400

    # Get SC24 program data
    programs = scrape_sc24_programs()
    program_details = "\n".join([f"{program['title']}: {program['description']}" for program in programs])

    # Create the prompt for OpenAI API
    prompt = f"User: {user_input}\n\nHere are some SC24 programs:\n{program_details}\n\nBot:"

    # Use Azure OpenAI API to generate a chatbot response
    try:
        response = openai.ChatCompletion.create(
            engine="gpt-4",  # Change if needed
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        bot_response = response.choices[0].message['content'].strip()
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"}), 500

# Serve the HTML page for the chatbot interface
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chatbot</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            #chatbox { border: 1px solid #ccc; width: 50%; height: 400px; padding: 10px; overflow-y: scroll; background-color: #f9f9f9; }
            .message { margin: 10px 0; }
            .message.user { text-align: right; color: blue; }
            .message.bot { text-align: left; color: green; }
        </style>
    </head>
    <body>
        <h2>Chat with our bot</h2>
        <div id="chatbox"></div>
        <input type="text" id="userInput" placeholder="Type your message here..." style="width: 50%; padding: 10px;">
        <button onclick="sendMessage()">Send</button>
        <script>
            function sendMessage() {
                let userInput = document.getElementById('userInput').value;
                if (userInput.trim() === '') return;
                let chatbox = document.getElementById('chatbox');
                chatbox.innerHTML += `<div class="message user">${userInput}</div>`;
                chatbox.scrollTop = chatbox.scrollHeight;
                document.getElementById('userInput').value = '';
                fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userInput })
                })
                .then(response => response.json())
                .then(data => {
                    chatbox.innerHTML += `<div class="message bot">${data.response}</div>`;
                    chatbox.scrollTop = chatbox.scrollHeight;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)

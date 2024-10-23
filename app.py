import openai
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

# Initialize Flask app
app = Flask(__name__)

# Azure OpenAI API credentials
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = "https://vinilhackproject.openai.azure.com/nexi"  # Replace with your Azure OpenAI API endpoint
openai.api_key = "10e4b0dd49924450b87d56aab5e4fc58"  # Replace with your Azure OpenAI API key

# Function to fetch data from the SC24 website
def scrape_sc24_website():
    url = 'https://sc24.supercomputing.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example: Extract all text from the page (you can customize based on the structure of the page)
    page_text = soup.get_text(separator='\n', strip=True)
    
    return page_text

# Function to query Azure OpenAI GPT-4 model
def ask_openai(question, context):
    response = openai.Completion.create(
        engine="gpt-4",  # Specify the GPT-4 engine
        prompt=f"Context: {context}\n\nQuestion: {question}",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response['choices'][0]['text'].strip()
    return answer

# Flask route for handling chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_question = data.get('question', '')

    # Fetch SC24 data (this can be optimized by caching)
    context_data = scrape_sc24_website()

    # Send the question along with website context to GPT-4
    gpt_answer = ask_openai(user_question, context_data)

    return jsonify({'answer': gpt_answer})

# Main function to run the app
if __name__ == '__main__':
    # Run Flask app (this can be integrated into your httpd webserver using WSGI)
    app.run(host='0.0.0.0', port=5000)

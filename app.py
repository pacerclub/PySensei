import openai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)

def get_response_from_openai(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('question')
    if not user_input:
        return jsonify({'error': 'No question provided'}), 400

    messages = [
        {"role": "system", "content": "You are a Python programming tutor. Help the user with their queries about learning Python."},
        {"role": "user", "content": user_input}
    ]

    response = get_response_from_openai(messages)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
import openai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
import markdown
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def convert_md_to_html(md_text, light_mode=True):
    html = markdown.markdown(md_text, extensions=['fenced_code', 'tables', 'toc', 'footnotes', 'attr_list', 'md_in_html'])
    soup = BeautifulSoup(html, 'lxml')

    for code in soup.find_all('code'):
        parent = code.parent
        if parent.name == 'pre':
            language = code.get('class', [''])[0].replace('language-', '') or 'text'
            lexer = get_lexer_by_name(language, stripall=True)
            formatter = HtmlFormatter(style='default' if light_mode else 'monokai')
            highlighted_code = highlight(code.string, lexer, formatter)
            code.replace_with(BeautifulSoup(highlighted_code, 'lxml'))

            copy_button_html = f'''
            <div class="code-header">
                <span class="language-label">{language}</span>
                <button class="copy-button" onclick="copyCode(this)">
                    <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon">
                        <path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path>
                        <path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path>
                    </svg>
                </button>
            </div>
            '''
            parent.insert_before(BeautifulSoup(copy_button_html, 'lxml'))

    return soup.prettify()

@app.route('/')
def home():
    if 'conversation' not in session:
        session['conversation'] = []
    return render_template('index.html', messages=session['conversation'])

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('question')
    if not user_input:
        return jsonify({'error': 'No question provided'}), 400

    messages = session.get('conversation', [])

    messages.append({"role": "user", "content": user_input})

    openai_messages = [
        {"role": "system", "content": "You are a Python programming tutor. Help the user with their queries about learning Python."},
        *messages
    ]

    response = get_response_from_openai(openai_messages)
    messages.append({"role": "assistant", "content": response})

    session['conversation'] = messages

    return jsonify({'response': response})

@app.route('/new_conversation', methods=['POST'])
def new_conversation():
    session.pop('conversation', None)
    return jsonify({'message': 'New conversation started'})

def get_response_from_openai(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.5,
        )
        return convert_md_to_html(response.choices[0].message.content.strip())
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
# app.py
import os
import json
from flask import Flask, render_template, request, redirect, url_for
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

openai.api_key = OPENAI_API_KEY
openai.api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')

# Default model and parameters
DEFAULT_PARAMS = {
    'model': 'gpt-4',  # Ensure this is a valid model name
    'temperature': 0.7,
    'top_p': 1.0,
    'max_tokens': 150,
    'presence_penalty': 0.0,
    'frequency_penalty': 0.0,
    'logit_bias': None,
    'user': None
}

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chat():
    params = DEFAULT_PARAMS.copy()
    bot_response = None
    user_input = None

    if request.method == 'POST':
        if 'reset' in request.form:
            return redirect(url_for('chat'))

        user_input = request.form.get('user_input', '').strip()
        params.update({
            'model': request.form.get('model', params['model']),
            'temperature': float(request.form.get('temperature', params['temperature'])),
            'top_p': float(request.form.get('top_p', params['top_p'])),
            'max_tokens': int(request.form.get('max_tokens', params['max_tokens'])),
            'presence_penalty': float(request.form.get('presence_penalty', params['presence_penalty'])),
            'frequency_penalty': float(request.form.get('frequency_penalty', params['frequency_penalty'])),
            'logit_bias': request.form.get('logit_bias') or None,
            'user': request.form.get('user') or None
        })

        # Parse logit_bias if provided
        if params['logit_bias']:
            try:
                params['logit_bias'] = json.loads(params['logit_bias'])
            except json.JSONDecodeError:
                bot_response = "Error: logit_bias must be a valid JSON object."
                return render_template('chat.html', bot_response=bot_response, user_input=user_input, **params)

        # Prepare messages
        messages = [{"role": "user", "content": user_input}]

        # Call OpenAI API using the correct method
        try:
            response = openai.ChatCompletion.create(
                model=params['model'],
                messages=messages,
                temperature=params['temperature'],
                top_p=params['top_p'],
                max_tokens=params['max_tokens'],
                presence_penalty=params['presence_penalty'],
                frequency_penalty=params['frequency_penalty'],
                logit_bias=params['logit_bias'],
                user=params['user']
            )
            bot_response = response['choices'][0]['message']['content'].strip()
        except Exception as e:
            bot_response = f"Error: {str(e)}"

    return render_template('chat.html', user_input=user_input, bot_response=bot_response, **params)

if __name__ == '__main__':
    app.run(debug=True)

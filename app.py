import os
from flask import Flask, render_template, request, redirect, url_for
import openai
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Default model and parameters
DEFAULT_PARAMS = {
    'model': 'gpt-4o-mini',
    'temperature': 0.7,
    'top_p': 1.0,
    'max_tokens': 150,
    'presence_penalty': 0.0,
    'frequency_penalty': 0.0,
    'logit_bias': None,
    'user': None
}

# Place to change API URL if needed
openai.api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chat():
    params = DEFAULT_PARAMS.copy()
    bot_response = None
    user_input = None

    if request.method == 'POST':
        if 'reset' in request.form:
            return redirect(url_for('chat'))

        user_input = request.form['user_input']
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
            bot_response = response['choices'][0]['message']['content']
        except Exception as e:
            bot_response = f"Error: {str(e)}"

    return render_template('chat.html', user_input=user_input, bot_response=bot_response, **params)

if __name__ == '__main__':
    app.run(debug=True)

# QuickChat - Hugging Face Chatbot

A minimalistic and configurable Python web application for chatting with Hugging Face's language models. This application provides an easy-to-use interface for interacting with various pre-trained models while allowing fine-tuned control over generation parameters.

## Features

- Clean, modern web interface
- Support for any Hugging Face conversational model
- Configurable model parameters:
  - Temperature
  - Top P
  - Max Length
  - Repetition Penalty
  - Top K
  - Sampling settings
- Real-time parameter adjustment
- Mobile-responsive design

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.template` to `.env` and add your Hugging Face API key:
   ```bash
   cp .env.template .env
   ```
5. Edit `.env` and replace `your_huggingface_api_key_here` with your actual Hugging Face API key

## Running the Application

1. Activate the virtual environment if not already activated:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to `http://localhost:5000`

## Model Parameters

- **Model Name**: The name of the Hugging Face model to use (e.g., "microsoft/DialoGPT-medium")
- **Temperature**: Controls randomness in the output (0.0 to 2.0)
- **Top P**: Nucleus sampling parameter (0.0 to 1.0)
- **Max Length**: Maximum length of generated text
- **Repetition Penalty**: Prevents repetitive text (1.0 to 2.0)
- **Top K**: Number of highest probability vocabulary tokens to keep
- **Sampling**: Enable/disable random sampling

## Default Model

The application uses `microsoft/DialoGPT-medium` as the default model, but you can easily switch to any other conversational model available on Hugging Face.

## Requirements

- Python 3.7+
- Flask
- Transformers
- PyTorch
- python-dotenv

## Security Note

Never commit your `.env` file containing your API key. The `.gitignore` file is configured to exclude it.

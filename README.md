# ChatBot Script using OpenAI API

This is a simple Python script that uses the OpenAI API to generate responses to user input, creating a basic chatbot. The chatbot uses the GPT-3.5-Turbo model to generate responses.

## Installation

To run this script, you'll need to have an OpenAI API key. You can sign up for one [here](https://beta.openai.com/signup/). Once you have a key, make sure to set it as an environment variable in your terminal:

```
export OPENAI_API_KEY=your_api_key_here
```

You'll also need to have the `openai` and `chardet` Python packages installed. You can install these using pip:

```
pip install openai chardet
```

## Usage

To use the chatbot, simply run the `chatbot.py` file from your terminal:

```
python chatbot.py
```

This will start the chatbot, and it will prompt you to enter a message. You can type in any message, and the chatbot will respond with a generated message.

To load a file of code snippets for the chatbot to explain, type "load_file" instead of a message. The chatbot will prompt you to enter the name of a file, and it will load the code snippets from that file and explain them to you.

To exit the chatbot, simply type "exit" and hit enter.

## Example

```
$ python chatbot.py
You: load_file
Enter file name: main.py

gpt: This is a Python script that uses the OpenAI API to create a customer service chatbot. It takes user input and sends it to the OpenAI API for processing. It uses the GPT-3.5-Turbo model to generate a response, which it then returns to the user.
```
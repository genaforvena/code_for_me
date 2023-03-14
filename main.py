import openai as ai
import chardet
import os

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("OpenAI API key not found. Please do export OPENAI_API_KEY=<your_api_key> and try again.")
    exit()

message_history = [
    {"role": "user", "content": "I'll send you my code file by file and you'll understand and remember it. "
                                "Some of them might be divided into multiple messages."
                                "The code will be enclosed in triple backticks like this ```. "
                                "After that I'll be asking you questions about the code. And you will reply my with code snippets. Say OK if you understood"},
    {"role": "assistant", "content": "OK"}
]


def predict(inp: str):
    if not inp:
        print("Please input a valid message.")
        return

    CHUNK_SIZE = 3500
    chunks = []
    # tokenize the new input sentence
    if len(inp) > CHUNK_SIZE:
        # split the input by lines and add lines iteratively to chunks
        current_chunk = ""
        for line in inp.split("\n"):
            if len(current_chunk + "\n" + line) <= CHUNK_SIZE:
                current_chunk += "\n" + line
            else:
                chunks.append(current_chunk[1:]) # remove the leading newline character
                current_chunk = line

        # append any remaining lines
        if current_chunk:
            chunks.append(current_chunk[1:])

    else:
        chunks = [inp]

    # append each chunk to message_history with user role
    for chunk in chunks:
        message_history.append({"role": "user", "content": f"{chunk}"})

    try:
        completion = ai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_history
        )
        # Just the reply text
        reply_content = completion.choices[0].message.content

        message_history.append({"role": "assistant", "content": f"{reply_content}"})

        # get pairs of msg["content"] from message history, skipping the pre-prompt here.
        response = [(message_history[i]["content"], message_history[i + 1]["content"]) for i in
                    range(max(0, len(message_history) - 2), len(message_history) - 1)]
        # Convert response to an iterable of dictionaries and add to conversation history
        for pair in response:
            message_history.append({"role": "assistant", "content": f"{pair[0]}"})
            message_history.append({"role": "user", "content": f"{pair[1]}"})

        # Print the reply
        print("\n")
        print("gpt: " + reply_content)
        print("\n")

    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def read_file(file):
    try:
        with open(file, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
            if not encoding:
                print(f"Unable to determine encoding for {file}, skipping...")
                return None
            with open(file, 'r', encoding=encoding) as fl:
                return "Here is my code:\n" + \
                        "```" + fl.read() + "```" + \
                        "\n Please read it and explain what it does."
    except FileNotFoundError:
        print(f"File {file} not found.")
    except Exception as e:
        print(f"Unexpected error while reading file {file}: {e}")
    return None


if __name__ == "__main__":
    ai.api_key = api_key

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break

        if user_input.lower() == "load_file":
            filename = input("Enter file name: ")
            file_contents = read_file(filename)
            if file_contents is not None:
                predict(file_contents)
        else:
            predict(user_input)
import openai as ai
import chardet
import os

api_key = os.environ.get("OPENAI_API_KEY")

message_history = [
    {"role": "user", "content": "I'll send you the code. "
                                "The content might be divided into multiple messages."
                                "The contents will be enclosed in triple backticks like this ```. "
                                "After that I'll be asking you questions about the code. "
                                "You will be answering with code snippets as much as possible. "
                                "Say OK if you understood"},
    {"role": "assistant", "content": "OK"}
]


def predict(inp: str):
    if not inp:
        print("Please input a valid message.")
        return

    CHUNK_SIZE = 2048
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

    # purge old messages if message_history limit is reached
    while len(message_history) > 24:
        message_history.pop(0)

    try:
        completion = ai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_history
        )
        # Just the reply text
        reply_content = completion.choices[0].message.content

        message_history.append({"role": "assistant", "content": f"{reply_content}"})

        # Print the reply
        print("\n")
        print("gpt: " + reply_content)
        print("\n")

    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def summarize_text(text):
    print(f"Summarizing text: {text}")
    MAX_CHUNK_SIZE = 2056  # Maximum size of each chunk of text that can be summarized by the model
    CHUNK_DELIMITER = "\n"  # Delimiter to use between chunks of text

    # Divide the text into chunks that can be summarized by the model without hitting the token limit
    chunks = []
    current_chunk = ""
    for sentence in text.split("."):
        if len(current_chunk + "." + sentence) <= MAX_CHUNK_SIZE:
            current_chunk += "." + sentence
        else:
            chunks.append(current_chunk[1:])  # Remove the leading period
            current_chunk = sentence

    # Append any remaining sentence
    if current_chunk:
        chunks.append(current_chunk[1:])

    # Generate summaries for each chunk of text
    summaries = []
    for chunk in chunks:
        print("\n\n")
        print("Generating summary for chunk...")
        context = [
            {"role": "user", "content": "I'll send you the text. "
                                        "Please summarize the following text in one or two sentences. "
                                        "Say OK if you understood"},
            {"role": "assistant", "content": "OK"},
            {"role": "user", "content": f"{chunk}"},
        ]
        print("Chunk: " + chunk)
        completion = ai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=context,
        )
        summary = completion.choices[0].message.content
        print("\n")
        print(f"Summary: {summary}")
        summaries.append(summary)
        print("\n")
        print("Summaries: " + str(summaries))

    # Combine the summaries into a single text
    final_summary = CHUNK_DELIMITER.join(summaries)
    print(f"Final summary: {final_summary}")

    # If the final summary is too long, recursively summarize it again
    if len(final_summary) > MAX_CHUNK_SIZE:
        return summarize_text(final_summary)

    context = [
        {"role": "user", "content": "I'll send you the text. "
                                    "Please summarize it into 500 words or something around like that."
                                    "Please keep the main points in the text and try to avoid repeating the same points."
                                    "Say OK if you understood"},
        {"role": "assistant", "content": "OK"},
        {"role": "user", "content": f"{final_summary}"},
    ]

    completion = ai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context,
    )

    final_summary = completion.choices[0].message.content

    return final_summary


def read_text_file(file):
    try:
        with open(file, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
            if not encoding:
                print(f"Unable to determine encoding for {file}, skipping...")
                return None
            with open(file, 'r', encoding=encoding) as fl:
                return fl.read()
    except FileNotFoundError:
        print(f"File {file} not found.")
    except Exception as e:
        print(f"Unexpected error while reading file {file}: {e}")
    return None


def read_code_file(file):
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
    if not api_key:
        print("OpenAI API key not found. Please do export OPENAI_API_KEY=<your_api_key> and try again.")
        exit()
    ai.api_key = api_key

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break

        if user_input.lower() == "load_file":
            filename = input("Enter file name: ")
            file_contents = read_code_file(filename)
            if file_contents is not None:
                predict(file_contents)

        if user_input.lower() == "summarize_text":
            filename = input("Enter file name: ")
            file_contents = read_text_file(filename)
            if file_contents is not None:
                summary = summarize_text(file_contents)
                print(summary)
        else:
            predict(user_input)
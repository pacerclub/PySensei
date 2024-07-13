import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)


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


def main():
    print("Welcome to CodeMotor: Your Personalized Python Learning Assistant!")
    print("Type 'exit' to end the session.")

    messages = [
        {"role": "system",
         "content": "You are a Python programming tutor. Help the user with their queries about learning Python."}
    ]

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Add user input to the conversation
        messages.append({"role": "user", "content": user_input})

        # Get response from OpenAI
        response = get_response_from_openai(messages)

        # Add assistant response to the conversation
        messages.append({"role": "assistant", "content": response})

        print(f"\nCodeMotor: {response}")


if __name__ == "__main__":
    main()
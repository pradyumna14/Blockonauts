import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
CORS(app)


openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
openai.api_key = openai_api_key  # Correct way to set the API key

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        response = openai.ChatCompletion.create(  # Correct method for chat completions
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are an AI doctor. Provide medical advice, but always recommend consulting a real doctor."},
                {"role": "user", "content": user_message}
            ]
        )

        return jsonify({"response": response.choices[0].message["content"]})

    except openai.OpenAIError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
from google.cloud import texttospeech
import base64
import io

app = Flask(__name__)
vertexai.init(project="devfest-pwani-442509", location="us-central1")

# Initialize speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Initialize text-to-speech
text_to_speech_client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Gemini model
gemini_model = GenerativeModel("gemini-1.5-flash-002")

def generate_response(user_input):
    try:
        chat = gemini_model.start_chat()
        response = chat.send_message(user_input, generation_config={"temperature": 0.7, "max_output_tokens": 256})
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

def synthesize_speech(text):
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = text_to_speech_client.synthesize_speech(
            request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
        )
        return response.audio_content
    except Exception as e:
        return None

def transcribe_audio(audio_data):
    try:
        with io.BytesIO(audio_data) as audio_file:
            audio = recognizer.recognize_google(recognizer.AudioFile(audio_file))
            return audio
    except Exception as e:
        return f"Error transcribing audio: {e}"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/process_audio", methods=["POST"])
def process_audio():
    try:
        audio_data = request.data
        user_input = transcribe_audio(audio_data)
        if user_input:
            response_text = generate_response(user_input)
            mp3_audio = synthesize_speech(response_text)

            if mp3_audio:
                encoded_audio = base64.b64encode(mp3_audio).decode("utf-8")
                return jsonify({"audio": encoded_audio, "text": response_text})
            else:
                return jsonify({"error": "Could not synthesize speech"}), 500
        else:
            return jsonify({"error": "Could not transcribe audio"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")



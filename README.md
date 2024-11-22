**Prerequisites**
Python 3.9+ Visit Python.org to download and install Python.
Basic knowledge of Python, Flask, and HTML
Google Cloud Project with Gemini API access

Step 1**Creating a simple program that accepts imput from microphone**

import speech_recognition as sr
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part

# innitializing the recognition
r = sr.Recognizer()

# Set the microphone as the source of audio
mic = sr.Microphone()

# Continuously listen for speech
with mic as source:
    print("Speak now.....")
    audio = r.listen(source)

        # Convert the audio to text
        text = r.recognize_google(audio)
        print("User:", text)  # Print user's input clearly
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition Service; {}".format(e))

		Step 2: **Extract Code from Vertex AI**
	# Adding the Vertex AI code

def multiturn_generate_content(user_input):
    vertexai.init(project="devfest-pwani-442509", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
    )
    chat = model.start_chat()
    response = chat.send_message(user_input,
                                 generation_config=generation_config,
                                 safety_settings=safety_settings)
    # Extract and return ONLY the text from the response
    return response.text

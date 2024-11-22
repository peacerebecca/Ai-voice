#**Prerequisites**
Python 3.9+ Visit Python.org to download and install Python.
Basic knowledge of Python, Flask, and HTML
Google Cloud Project with Gemini API access

#Step 1: **Creating a simple program that accepts imput from microphone**

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

#Step 2: **Extract Code from Vertex AI**
	
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
     		generation_config = {
   	 "max_output_tokens": 8192,
   	 "temperature": 1,
   	 "top_p": 0.95,
	}

	safety_settings = [
  	  SafetySetting(
       	 category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
   	 ),
   	 SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    	),
    	SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
   	 ),
   	 SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
   	 ),
	]


    	user_text = r.recognize_google(audio)
    	bot_response = multiturn_generate_content(user_text)
    	print("ChatBot:", bot_response) #Print the bot's response clearly

	except Exception as e:
   	 print(f"An error occurred: {e}")

Step 3: **Creating a function to read text output into speech**
	#User input text to speech
	"""Synthesizes speech from the input string of text."""
	from google.cloud import texttospeech

	client = texttospeech.TextToSpeechClient()

	input_text = texttospeech.SynthesisInput(text= bot_response)

	# Note: the voice can also be specified by name.
	# Names of voices can be retrieved with client.list_voices().
	voice = texttospeech.VoiceSelectionParams(
	    language_code="en-US",
 	   name="en-US-Studio-O",
	)

	audio_config = texttospeech.AudioConfig(
   	 audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    	speaking_rate=1
	)

	response = client.synthesize_speech(
    	request={"input": input_text, "voice": voice, "audio_config": audio_config}
	)

	# The response's audio_content is binary.
	with open("output.mp3", "wb") as out:
  	  out.write(response.audio_content)
  	  print('Bot Audio "output.mp3"')

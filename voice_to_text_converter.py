import speech_recognition as sr
from gtts import gTTS
import os


def voice_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google_cloud(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))


def text_to_speech(text, output_file):
    # Create a gTTS object
    tts = gTTS(text=text, lang='en')

    # Save the audio file
    tts.save(output_file)

    # Play the audio file (optional)
    os.system("afplay {}".format(output_file))  # macOS


if __name__ == '__main__':
    text = voice_to_text()
    text = 'To pronounce this sentence correctly: ' + text
    text_to_speech(text, 'output.mp3')

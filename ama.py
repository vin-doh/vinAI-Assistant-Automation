import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

# Set the voice to a female voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Select the index of the desired voice

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2-medium"  # You can try other variants like "gpt2-large" or "gpt2-xl"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def get_audio_input(timeout=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=timeout)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-us')
            print(query)
            return query.lower()
        except sr.WaitTimeoutError:
            print("Timeout waiting for audio.")
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"

def time():
    current_time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is " + current_time)

def date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak("The current date is " + current_date)

def wishme():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning Vincent!")
    elif 12 <= hour < 18:
        speak("Good afternoon Vincent")
    elif 18 <= hour < 24:
        speak("Good evening Vincent")
    else:
        speak("Good night Vincent")
    speak("Vincent, how can I assist you?")

def send_email(to, content):
    # Use email_user and email_password environment variables
    email_user = os.environ.get('EMAIL_USER')
    email_password = os.environ.get('EMAIL_PASSWORD')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, to, content)
    server.close()

def open_web_browser(browser, search_query):
    browser_path = {
        'firefox': 'C:/Program Files/Mozilla Firefox/firefox.exe',
        'chrome': 'C:/Program Files/Google/Chrome/Application/chrome.exe',
        'edge': 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
    }
    if browser in browser_path:
        webbrowser_path = browser_path[browser]
        wb.get(webbrowser_path).open_new_tab(search_query)
    else:
        speak("Sorry, I don't support that web browser.")

def take_screenshot():
    screenshot_dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'vinAI', 'ss')
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    screenshot_path = os.path.join(screenshot_dir, 'ss.png')
    img = pyautogui.screenshot()
    img.save(screenshot_path)
    speak("Screenshot saved.")

def get_cpu_usage():
    usage = str(psutil.cpu_percent()) + '%'
    speak("CPU is at " + usage + " now.")
    battery = psutil.sensors_battery()
    speak("Battery is at " + str(battery.percent) + " percent.")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def gpt2_response(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=100, num_return_sequences=1, no_repeat_ngram_size=2)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    speak("Initializing...")
    wishme()
    while True:
        query = get_audio_input()

        if 'time' in query:
            time()
        elif 'date' in query:
            date()
        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            print(result)
            speak(result)
        elif 'send email' in query:
            try:
                speak("What should I say, Vincent?")
                content = get_audio_input(timeout=10)
                to = "kennedydziworshie00@gmail.com"
                send_email(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Unable to send email.")

        # ... (other tasks)

        elif 'ask a question' in query:
            speak("Sure, what question would you like to ask?")
            question = get_audio_input()
            gpt2_prompt = f"You asked: {question}"
            gpt2_response_text = gpt2_response(gpt2_prompt)
            speak("You asked: " + question)
            speak("GPT-2's response:")
            speak(gpt2_response_text)
            
        elif 'offline' in query:
            speak("Goodbye Vincent.")
            break

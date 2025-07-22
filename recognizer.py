import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.pause_threshold = 0.8
    
    with sr.Microphone() as source:
        print("🎧 Adjusting noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("🎧 Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            text = r.recognize_google(audio).lower()
            print(f"Recognized: {text}")
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"API error: {e}")
            return "internet error"
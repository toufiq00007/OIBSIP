import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys
import time

# --- Configuration and Initialization ---pip install Flask pyjokes wikipedia pywhatkit

WAKE_WORD = 'alexa'
listener = sr.Recognizer()
engine = pyttsx3.init()

# Get available voices and set a preferred voice (with fallback)
try:
    voices = engine.getProperty('voices')
    # Try setting to the second voice (index 1) for a female voice, common on many systems
    engine.setProperty('voice', voices[1].id)
except IndexError:
    # Fallback to the default system voice
    print("Warning: Could not set preferred voice. Using system default.")
    pass


# --- Helper Functions (Core Logic) ---

def talk(text):
    """
    Speaks the given text using the TTS engine.
    Uses runAndWait() to ensure full speech synchronization.
    """
    print(f"Assistant: {text}")
    engine.say(text)
    # Critical for preventing speech truncation/silence in a loop
    engine.runAndWait()


def take_command():
    """
    Listens for a command from the microphone, processes it, and returns a cleaned string.
    """
    command = ''
    with sr.Microphone() as source:
        print('Listening...')
        # Adjust for ambient noise for better accuracy
        listener.adjust_for_ambient_noise(source, duration=0.5)

        try:
            voice = listener.listen(source, timeout=5, phrase_time_limit=10)
            command = listener.recognize_google(voice)
            command = command.lower()

            if WAKE_WORD in command:
                command = command.replace(WAKE_WORD, '').strip()

            if command:
                print(f"User said: {command}")

        except sr.WaitTimeoutError:
            # Silence detected after a certain period
            pass
        except sr.UnknownValueError:
            # Speech was heard, but not understandable
            # print("Sorry, I did not catch that.") # Suppress this print for smoother loop
            pass
        except sr.RequestError as e:
            # Issue with Google Speech Recognition service (e.g., no internet)
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            # Catching other unexpected errors
            print(f"An unexpected error occurred: {e}")

    return command.strip()


# --- Command Execution Functions ---

def play_song(command):
    """Plays a song on YouTube based on the command."""
    song = command.replace('play', '').strip()
    if not song:
        talk("Please specify a song or artist to play.")
        return

    talk(f'playing {song} on YouTube')
    pywhatkit.playonyt(song)


def get_time(_):
    """Tells the current time."""
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    talk(f'Current time is {current_time}')


def get_date(_):
    """Tells the current date."""
    today = datetime.datetime.now().strftime('%A, %B %d, %Y')
    talk(f"Today's date is {today}")


def tell_joke(_):
    """Tells a random joke."""
    joke = pyjokes.get_joke()
    talk(joke)


def relationship_status(_):
    """Provides a humorous answer about its relationship status."""
    talk('I am in a committed relationship with my dedicated server and Wi-Fi connection.')


def wikipedia_search(command):
    """Searches Wikipedia based on the command."""
    person = command.replace('who the heck is', '').replace('tell me about', '').strip()

    if not person:
        talk("Please tell me who you want to search for.")
        return

    talk(f"Searching Wikipedia for {person}")
    try:
        # Fetch the first sentence summary
        info = wikipedia.summary(person, sentences=1, auto_suggest=False)
        talk(info)
    except wikipedia.exceptions.PageError:
        talk(f"Sorry, I couldn't find any Wikipedia information about {person}.")
    except Exception:
        talk("Sorry, I ran into an error fetching that information.")


def handle_exit(_):
    """Exits the assistant application."""
    talk('Goodbye! Have a nice day.')
    # Using a global flag/return value is safer than sys.exit() inside a loop,
    # but for simplicity, we'll use sys.exit() as in your original script.
    sys.exit()


def default_response(_):
    """Handles commands that weren't matched."""
    talk('I didn\'t recognize that command. Try asking about the time, a person, or to play a song.')


# --- Command Mapping Dictionary ---

# Organize commands from most specific (phrase) to most general (keyword)
COMMAND_MAP = {
    # Full Phrase Commands (Highest Priority)
    'are you single': relationship_status,
    'who the heck is': wikipedia_search,  # Note: This will catch 'tell me about' too
    'tell me about': wikipedia_search,
    'goodbye': handle_exit,

    # Keyword Commands (Medium Priority)
    'joke': tell_joke,
    'play': play_song,
    'time': get_time,
    'date': get_date,
    'stop': handle_exit,
    'exit': handle_exit
}


def run_alexa():
    """
    The main logic function that retrieves a command and executes the corresponding action.
    """
    command = take_command()

    if command == '':
        return  # Skip if no command was recognized

    # Iterate through the command map to find the best match
    for trigger, function in COMMAND_MAP.items():
        if trigger in command:
            # Execute the function associated with the trigger
            function(command)
            return  # Exit the loop after the first match is executed

    # If no command matched, execute the default response
    default_response(command)


# --- Main Execution Loop ---
if __name__ == '__main__':
    talk(f"Hello, I am ready. Say '{WAKE_WORD}, play a song' or '{WAKE_WORD}, what is the time'.")
    while True:
        run_alexa()
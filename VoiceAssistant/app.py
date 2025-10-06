import pywhatkit
import datetime
import wikipedia
import pyjokes
from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- NEW: Import CORS

# --- 1. Configuration and Initialization ---
# NOTE: TTS (pyttsx3) and Microphone (sr) dependencies are REMOVED.

app = Flask(__name__)
CORS(app)  # <--- NEW: Enable CORS for all routes

WAKE_WORD = 'alexa'
ASSISTANT_RESPONSE_TEXT = ""


# --- 2. Helper Function ---

def talk(text):
    """Stores the text to be returned via the API response."""
    global ASSISTANT_RESPONSE_TEXT
    print(f"[Backend Log] Assistant: {text}")
    ASSISTANT_RESPONSE_TEXT = text


# --- 3. Command Execution Functions ---

def play_song(command):
    """Plays a song on YouTube based on the command."""
    song = command.replace('play', '').strip()
    if not song:
        talk("Please specify a song or artist to play.")
        return

    talk(f'Playing {song} on YouTube. (Check the server machine for the browser window.)')
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

    try:
        info = wikipedia.summary(person, sentences=1, auto_suggest=False)
        talk(info)
    except wikipedia.exceptions.PageError:
        talk(f"Sorry, I couldn't find any Wikipedia information about {person}.")
    except Exception:
        talk("Sorry, I ran into an error fetching that information.")


def handle_exit(_):
    """Confirms the exit command but keeps the server running."""
    talk('The server received a shutdown command, but it will remain running. Goodbye!')


def default_response(_):
    """Handles commands that weren't matched."""
    talk("I didn't recognize that command. Try asking about the time, a person, or to play a song.")


# --- 4. Command Mapping Dictionary ---
COMMAND_MAP = {
    'are you single': relationship_status,
    'who the heck is': wikipedia_search,
    'tell me about': wikipedia_search,
    'goodbye': handle_exit,
    'stop listening': handle_exit,

    'joke': tell_joke,
    'play': play_song,
    'time': get_time,
    'date': get_date,
    'stop': handle_exit,
    'exit': handle_exit
}


def run_command_logic(command):
    """Executes the command logic based on the text input and returns the response."""
    global ASSISTANT_RESPONSE_TEXT
    ASSISTANT_RESPONSE_TEXT = ""

    command = command.lower().strip()

    if not command:
        talk("Please provide a command.")
        return ASSISTANT_RESPONSE_TEXT

    if WAKE_WORD in command:
        command = command.replace(WAKE_WORD, '').strip()

    found_command = False
    for trigger, function in COMMAND_MAP.items():
        if trigger in command:
            if trigger == 'play' and 'joke' in command:
                continue

            print(f"[Backend Log] Trigger matched: '{trigger}' for command: '{command}'")
            function(command)
            found_command = True
            break

    if not found_command:
        default_response(command)

    return ASSISTANT_RESPONSE_TEXT


# --- 5. Flask API Endpoint ---

@app.route('/command', methods=['GET', 'POST'])
def handle_command():
    """Receives command text and returns a JSON response."""
    try:
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400

        data = request.get_json()
        command_text = data.get('command', '')

        if not command_text:
            return jsonify({"error": "Missing 'command' field in JSON"}), 400

        response_text = run_command_logic(command_text)

        return jsonify({
            "status": "success",
            "command_received": command_text,
            "assistant_response": response_text
        })
    except Exception as e:
        print(f"[ERROR] API Handler failed: {e}")
        return jsonify({
            "status": "error",
            "message": f"An internal server error occurred: {str(e)}",
            "assistant_response": "Sorry, I ran into a technical problem while processing your request."
        }), 500


# --- 6. Main Execution ---
if __name__ == '__main__':
    print("\n--- VOICE ASSISTANT FLASK BACKEND STARTING ---")
    print(f"API is available at: http://127.0.0.1:5000/command (POST)")
    print("Ensure the frontend is open and pointing to this address.")
    # Use host='0.0.0.0' for wider local access if needed, but '127.0.0.1' is fine for development.
    app.run(debug=True, port=5000, host='127.0.0.1')
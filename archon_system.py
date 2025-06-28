# Project Archon
# Phase 2: Auditory System Integration

import subprocess
import vosk
import sounddevice as sd
import queue
import json
import os

# --- CONFIGURATION ---
ASSISTANT_NAME = "Archon"
USER_NAME = "Sir"
MODEL_PATH = "model/vosk-model-small-id-0.4" # Pastikan path ini sesuai dengan nama folder model Anda
SAMPLE_RATE = 16000
# ---------------------------

# --- VALIDATION ---
if not os.path.exists(MODEL_PATH):
    print(f"[{ASSISTANT_NAME}]: FATAL ERROR: Vosk model not found at '{MODEL_PATH}'.")
    print(f"[{ASSISTANT_NAME}]: Please make sure you have downloaded the model and placed it correctly.")
    exit()
# ---------------------------

q = queue.Queue()

def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

def listen_for_command():
    """
    Captures audio from the microphone and uses Vosk to recognize speech.
    This is Archon's 'ear'.
    """
    model = vosk.Model(MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    print(f"\n[{ASSISTANT_NAME}]: Listening...")
    
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result_json = recognizer.Result()
                result_dict = json.loads(result_json)
                recognized_text = result_dict['text']
                
                if recognized_text: # Hanya proses jika ada teks yang dikenali
                    print(f"[{ASSISTANT_NAME}]: Voice detected: '{recognized_text}'")
                    return recognized_text
            # else:
            #     # Optional: print partial results for feedback
            #     partial_result = json.loads(recognizer.PartialResult())['partial']
            #     if partial_result:
            #         print(f"[{ASSISTANT_NAME}]: ...{partial_result}...")

def execute_shell_command(command_to_run):
    """Executes a command in the system's shell and captures the output."""
    print(f"\n[{ASSISTANT_NAME}]: Executing command: '{command_to_run}'...")
    try:
        result = subprocess.run(command_to_run, capture_output=True, text=True, shell=True, check=True)
        if result.stdout:
            print(f"[{ASSISTANT_NAME}]: Output:\n---")
            print(result.stdout)
            print("---\n")
        else:
            print(f"[{ASSISTANT_NAME}]: Command executed successfully with no output.\n")
    except subprocess.CalledProcessError as e:
        print(f"[{ASSISTANT_NAME}]: Error executing command.")
        if e.stderr:
            print(f"[{ASSISTANT_NAME}]: Error Details:\n---")
            print(e.stderr)
            print("---\n")
    except FileNotFoundError:
        print(f"[{ASSISTANT_NAME}]: Error: Command not found. Make sure it's a valid command.\n")


def execute_code_creation_action(command_detail):
    """A placeholder function for the code creation action."""
    print(f"\n[{ASSISTANT_NAME}]: Affirmative, {USER_NAME}. Initiating code generation protocol...")
    print(f"[{ASSISTANT_NAME}]: Analyzing request: '{command_detail}'")
    print(f"[{ASSISTANT_NAME}]: ... (Simulating local LLM call) ...")
    print(f"[{ASSISTANT_NAME}]: Protocol complete.\n")


def process_command(command):
    """This function acts as the 'brain' that processes the user's command."""
    if not command: # Jika perintah kosong, abaikan
        return True

    lower_command = command.lower()
    keywords_for_creation = ["create", "build", "make", "generate", "write"]
    keywords_for_program_type = ["program", "code", "script"]
    keywords_for_shell = ["run command", "execute", "run", "shell"]

    triggered_shell_keyword = next((word for word in keywords_for_shell if word in lower_command), None)
    if triggered_shell_keyword:
        command_to_run = command[command.find(triggered_shell_keyword) + len(triggered_shell_keyword):].strip()
        if command_to_run:
            execute_shell_command(command_to_run)
        else:
            print(f"[{ASSISTANT_NAME}]: Please specify a command to run, {USER_NAME}.\n")
    elif any(word in lower_command for word in keywords_for_creation) and \
       any(word in lower_command for word in keywords_for_program_type):
        execute_code_creation_action(command)
    elif "exit" in lower_command or "shutdown" in lower_command:
        print(f"[{ASSISTANT_NAME}]: System shutting down. Goodbye, {USER_NAME}.")
        return False
    else:
        print(f"[{ASSISTANT_NAME}]: Command not recognized, {USER_NAME}. Please try again.\n")
    return True


def main():
    """The main function of the program."""
    print("="*40)
    print(f"WELCOME TO {ASSISTANT_NAME.upper()} OS - v0.3 'Auditory Update'")
    print("System ready. Auditory module is active.")
    print("="*40)
    
    is_running = True
    while is_running:
        recognized_command = listen_for_command()
        is_running = process_command(recognized_command)


if __name__ == "__main__":
    main()
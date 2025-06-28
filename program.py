# Project Archon
# Phase 1: Core Logic Framework with Personalization (English Refactor)

# --- PERSONAL CONFIGURATION ---
ASSISTANT_NAME = "Archon"
USER_NAME = "Sir"
# ---------------------------

def execute_code_creation_action(command_detail):
    """
    A placeholder function for the code creation action.
    This is where we will eventually call the local LLM.
    """
    print(f"\n[{ASSISTANT_NAME}]: Affirmative, {USER_NAME}. Initiating code generation protocol...")
    print(f"[{ASSISTANT_NAME}]: Analyzing request: '{command_detail}'")
    print(f"[{ASSISTANT_NAME}]: ... (Simulating local LLM call) ...")
    # In Phase 3, the line above will be replaced with code to run the local LLM.
    print(f"[{ASSISTANT_NAME}]: Protocol complete.\n")


def process_command(command):
    """
    This function acts as the 'brain' that processes the user's command.
    """
    lower_command = command.lower()

    keywords_for_creation = ["create", "build", "make", "generate", "write"]
    keywords_for_program_type = ["program", "code", "script"]

    if any(word in lower_command for word in keywords_for_creation) and \
       any(word in lower_command for word in keywords_for_program_type):
        
        execute_code_creation_action(command)
    
    elif "exit" in lower_command or "shutdown" in lower_command:
        print(f"[{ASSISTANT_NAME}]: System shutting down. Goodbye, {USER_NAME}.")
        return False 
    
    else:
        print(f"[{ASSISTANT_NAME}]: Command not recognized, {USER_NAME}. Please try again.\n")
    
    return True


def main():
    """
    The main function of the program.
    """
    print("="*40)
    print(f"WELCOME TO {ASSISTANT_NAME.upper()} OS")
    print("System ready and waiting for your command.")
    print("="*40)
    
    is_running = True
    while is_running:
        user_command = input(f"{USER_NAME}: ")
        is_running = process_command(user_command)
if __name__ == "__main__":
    main()
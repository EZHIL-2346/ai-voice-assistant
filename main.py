import os
from dotenv import load_dotenv
from overlay import AssistantOverlay

def main():
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Missing OpenAI API key in .env file")
        return
        
    assistant = AssistantOverlay()
    assistant.run()

if __name__ == "__main__":
    # Only elevate if not already admin
    from modules.elevate import run_as_admin
    run_as_admin()
    main()
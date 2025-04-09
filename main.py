# main.py
from src.himalia import Himalia

def main():
    """Example usage of Himalia"""
    # Create a Himalia instance
    himalia = Himalia()
    
    # Process some input
    himalia.process_input("I'm feeling happy today!")
    
    # Print current emotional state
    print(himalia.get_status_report())
    
    # Generate a prompt for an LLM
    prompt = himalia.generate_prompt()
    print("\nGenerated prompt:")
    print(prompt)

if __name__ == "__main__":
    main()
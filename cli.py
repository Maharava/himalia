import argparse
import time
import datetime
import sys
from src.himalia import Himalia  # Update to import from the module structure

def print_color(text, color_code):
    """Print colored text"""
    print(f"\033[{color_code}m{text}\033[0m")

def main():
    parser = argparse.ArgumentParser(description="Himalia - Emotional LLM Prompt Generator")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--load", help="Load saved emotional state")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--simulate", type=int, help="Run a simulation for N steps", default=0)
    args = parser.parse_args()
    
    # Initialize Himalia
    himalia = Himalia(args.config)
    
    # Load saved state if specified
    if args.load:
        himalia.load_state(args.load)
        print_color(f"Loaded emotional state from {args.load}", 92)
    
    if args.interactive:
        interactive_mode(himalia)
    elif args.simulate > 0:
        simulation_mode(himalia, args.simulate)
    else:
        # Default behavior - show current state and generate a prompt
        print_color(himalia.get_status_report(), 96)
        print_color("\nGENERATED PROMPT:", 93)
        print_color(himalia.generate_prompt(), 97)

def interactive_mode(himalia):
    """Run Himalia in interactive mode"""
    print_color("=== HIMALIA INTERACTIVE MODE ===", 95)
    print_color("Type 'help' for commands, 'exit' to quit", 95)
    
    while True:
        try:
            user_input = input("\n> ")
            
            if user_input.lower() == 'exit':
                break
                
            elif user_input.lower() == 'help':
                print_color("Available commands:", 96)
                print("  status       - Show current emotional state")
                print("  prompt       - Generate emotional prompt")
                print("  set [emotion] [value] - Set emotion intensity (0.0-1.0)")
                print("  wait [minutes] - Simulate passage of time")
                print("  save [file]  - Save current state")
                print("  load [file]  - Load saved state")
                print("  reset        - Reset to default emotional state")
                print("  exit         - Exit the program")
                print("  <any other text> - Process as input for emotional analysis")
                
            elif user_input.lower() == 'status':
                print_color(himalia.get_status_report(), 96)
                
            elif user_input.lower() == 'prompt':
                print_color("GENERATED PROMPT:", 93)
                print_color(himalia.generate_prompt(), 97)
                
            elif user_input.lower().startswith('set '):
                parts = user_input.split()
                if len(parts) == 3:
                    emotion = parts[1].lower()
                    try:
                        value = float(parts[2])
                        if himalia.trigger_emotion(emotion, value, "Manual adjustment"):
                            print_color(f"Set {emotion} to {value}", 92)
                        else:
                            print_color(f"Unknown emotion: {emotion}", 91)
                    except ValueError:
                        print_color("Invalid value, must be a number between 0 and 1", 91)
                else:
                    print_color("Usage: set [emotion] [value]", 91)
                    
            elif user_input.lower().startswith('wait '):
                try:
                    minutes = float(user_input.split()[1])
                    himalia.update_emotional_state(minutes)
                    print_color(f"Simulated {minutes} minutes passing", 92)
                except (ValueError, IndexError):
                    print_color("Usage: wait [minutes]", 91)
                    
            elif user_input.lower().startswith('save '):
                filename = user_input[5:].strip()
                if himalia.save_state(filename):
                    print_color(f"State saved to {filename}", 92)
                    
            elif user_input.lower().startswith('load '):
                filename = user_input[5:].strip()
                if himalia.load_state(filename):
                    print_color(f"State loaded from {filename}", 92)
                    
            elif user_input.lower() == 'reset':
                himalia = Himalia()
                print_color("Emotional state reset to defaults", 92)
                
            else:
                # Process as emotional input
                himalia.process_input(user_input)
                print_color("Input processed. Updated emotional state:", 94)
                print_color(himalia.get_status_report(), 96)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print_color(f"Error: {e}", 91)
    
    print_color("Exiting Himalia interactive mode", 95)

def simulation_mode(himalia, steps):
    """Run an automated simulation"""
    print_color(f"=== RUNNING HIMALIA SIMULATION FOR {steps} STEPS ===", 95)
    print_color("Initial state:", 96)
    print_color(himalia.get_status_report(), 96)
    
    # Sample inputs for simulation
    sample_inputs = [
        "I'm really happy today!",
        "That makes me so angry.",
        "I'm worried about the future.",
        "This is fascinating and I'm curious to learn more.",
        "I trust your judgment on this matter.",
        "That's disappointing news.",
        "What a wonderful surprise!",
        "I'm looking forward to the results.",
        "That's absolutely disgusting behavior."
    ]
    
    for step in range(1, steps + 1):
        print_color(f"\n=== SIMULATION STEP {step} ===", 93)
        
        # Simulate time passing (5-30 minutes)
        time_passed = 5 + (step % 6) * 5
        
        # Every third step, process a random input
        if step % 3 == 0:
            input_text = sample_inputs[step % len(sample_inputs)]
            print_color(f"Processing input: '{input_text}'", 94)
            himalia.process_input(input_text, time_passed)
        else:
            # Just let time pass
            himalia.update_emotional_state(time_passed)
            print_color(f"Time passing: {time_passed} minutes", 94)
        
        # Show current state
        print_color("Current emotional state:", 96)
        print_color(himalia.get_status_report(), 96)
        
        # Generate prompt
        print_color("Generated prompt:", 92)
        print_color(himalia.generate_prompt(), 97)
        
        # Pause between steps
        if step < steps:
            time.sleep(1)
    
    print_color(f"\n=== SIMULATION COMPLETE ({steps} STEPS) ===", 95)

if __name__ == "__main__":
    main()
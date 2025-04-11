# Himalia Emotions API Reference

## 1. Overview

Himalia is an emotion simulation system that adds emotional state and memory to LLM responses. It simulates emotions, tracks their evolution over time, and generates emotion-aware prompts for integration with Large Language Models.

## 2. Installation & Setup

```python
# Import the Himalia module
from src.himalia_emotions.src.himalia import Himalia

# Create a Himalia instance with default personality
himalia = Himalia()

# Create with custom configuration file
himalia = Himalia(config_path="path/to/config.json")```
3. Core Classes
Himalia
Main orchestrator class for the emotion simulation system.

EmotionalState
Internal representation of emotions, dimensions, and memory.

PersonalityManager
Handles loading and validating personality configurations.

4. Basic Usage
Processing Input
```
# Process text input (updates emotional state)
himalia.process_input("I'm feeling happy today!")

# Process with simulated time passage (in minutes)
himalia.process_input("This makes me angry!", elapsed_minutes=30)
```
Getting Current State
```
# Get human-readable report of current emotional state
status_report = himalia.get_status_report()
print(status_report)

# Access specific emotions directly
joy_level = himalia.emotional_state.emotions["joy"]
anger_level = himalia.emotional_state.emotions["anger"]

# Access emotional dimensions
pleasure = himalia.emotional_state.dimensions["pleasure"]
arousal = himalia.emotional_state.dimensions["arousal"]
```
Generating Prompts
```
# Generate an emotional prompt for your LLM
prompt = himalia.generate_prompt()

# Use this prompt with your LLM
llm_input = f"{prompt}\n\nUser: {user_message}"
```
5. Time Simulation
```
# Update emotional state based on time passage (minutes)
elapsed_time = himalia.update_emotional_state(elapsed_minutes=15)
```
6. Emotion Manipulation
```
# Directly trigger an emotion with specific intensity (0.0-1.0)
himalia.trigger_emotion("joy", 0.7, "Found something exciting")

# LLM-based emotion analysis
analysis_prompt = himalia.generate_emotion_analysis_prompt("I love this so much!")
analysis_result = your_llm_function(analysis_prompt)
himalia.process_emotion_analysis(analysis_result)
```
7. State Persistence
```
# Save current emotional state to file
himalia.save_state("saved_state.json")

# Load emotional state from file
himalia.load_state("saved_state.json")
```
8. Personality System
Available Personalities
```
# Get list of available personality files
```
personalities = himalia.personality_manager.get_available_personalities()
```
Loading perosnalities
```
# Load specific personality
personality = himalia.personality_manager.load_personality("custom_personality.json")
```

Personality Structure
Personalities are defined in JSON with these key sections:

dimensions: Emotional dimensions (pleasure, arousal, etc.)
emotions: Individual emotions with baselines and relationships
personality_traits: Core traits affecting emotional processing
memory_capacity: Emotional memory capacity
contagion_settings: How emotions affect each other
emotion_trigger_settings: How inputs trigger emotions
9. Emotional Memory
Himalia maintains emotional memory of significant events that influence its state:

```
# Access recent memory (most recent first)
if himalia.emotional_state.emotional_memory:
    recent_memory = himalia.emotional_state.emotional_memory[-1]
    print(f"Recent emotion: {recent_memory['emotion']}")
    print(f"Reason: {recent_memory['reason']}")
    ```

11. Complete Method Reference
Himalia Class
__init__(config_path=None) - Initialize Himalia
process_input(input_text, elapsed_minutes=None) - Process text input
update_emotional_state(elapsed_minutes=None) - Update based on time passing
trigger_emotion(emotion, intensity, reason=None) - Directly trigger emotion
generate_prompt() - Generate emotional prompt for LLM
get_status_report() - Get human-readable emotion status
save_state(filepath) - Save emotional state to file
load_state(filepath) - Load emotional state from file
generate_emotion_analysis_prompt(text) - Create prompt for emotion analysis
process_emotion_analysis(result) - Process LLM emotion analysis response
PersonalityManager Class
get_available_personalities() - List available personality files
load_personality(filename) - Load personality configuration
save_personality(personality, filename) - Save personality configuration
12. Integration Example
```
from src.himalia_emotions.src.himalia import Himalia

# Initialize Himalia
himalia = Himalia()

# Function to process user messages
def process_user_message(user_message):
    # Update Himalia with the user's message
    himalia.process_input(user_message)
    
    # Generate an emotion-aware prompt
    emotion_prompt = himalia.generate_prompt()
    
    # Combine with user message for LLM
    full_prompt = f"{emotion_prompt}\n\nUser: {user_message}"
    
    # Send to your LLM and get response
    llm_response = your_llm_function(full_prompt)
    
    return llm_response

# Example usage
response = process_user_message("I'm feeling really happy today!")
```

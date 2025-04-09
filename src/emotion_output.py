# src/emotion_output.py
def generate_prompt(self) -> str:
    """Generate an emotional prompt based on current emotional state and config"""
    # Get dominant emotions (top 2)
    dominant_emotions = sorted(
        [(e, i) for e, i in self.emotional_state.emotions.items() if i > 0.2],
        key=lambda x: x[1],
        reverse=True
    )[:2]
    
    # Build the prompt
    prompt = "Your response should reflect the following emotional tone:\n\n"
    
    # Add dimensional guidance from config
    for dim_name, value in self.emotional_state.dimensions.items():
        dim_config = self.personality_config["dimensions"][dim_name]
        threshold = dim_config["prompt_rules"]["threshold"]
        
        if abs(value) > threshold:
            if value > 0:
                prompt += dim_config["prompt_rules"]["positive_text"] + "\n"
            else:
                prompt += dim_config["prompt_rules"]["negative_text"] + "\n"
    
    # Add specific emotion guidance from config
    if dominant_emotions:
        prompt += "\nYour primary emotional state includes:\n"
        
        for emotion, intensity in dominant_emotions:
            prompt += f"- {emotion.capitalize()} (intensity: {int(intensity * 100)}%)\n"
            
            # Get prompt rules from config
            emotion_config = self.personality_config["emotions"][emotion]
            threshold = emotion_config["prompt_rules"]["threshold"]
            
            if intensity > threshold:
                prompt += f"  {emotion_config['prompt_rules']['text']}\n"
    
    # Add context from emotional memory if relevant
    if self.emotional_state.emotional_memory:
        recent_memory = self.emotional_state.emotional_memory[-1]
        if recent_memory["intensity"] > 0.5:
            prompt += f"\nRecall your recent emotional experience of {recent_memory['emotion']} "
            prompt += f"because: {recent_memory['reason']}\n"
    
    return prompt

def get_status_report(self) -> str:
    """Generate a human-readable status report of the current emotional state"""
    report = "=== HIMALIA EMOTIONAL STATUS REPORT ===\n\n"
    
    # Dimensions section
    report += "EMOTIONAL DIMENSIONS:\n"
    for dim, value in self.emotional_state.dimensions.items():
        report += f"  {dim.capitalize()}: {value:.2f}\n"
    
    # Emotions section
    report += "\nEMOTIONAL INTENSITIES:\n"
    sorted_emotions = sorted(
        self.emotional_state.emotions.items(),
        key=lambda x: x[1],
        reverse=True
    )
    for emotion, intensity in sorted_emotions:
        report += f"  {emotion.capitalize()}: {intensity:.2f}\n"
    
    # Recent memory
    if self.emotional_state.emotional_memory:
        report += "\nRECENT EMOTIONAL EVENTS:\n"
        for i, memory in enumerate(reversed(self.emotional_state.emotional_memory)):
            if i >= 3:  # Show only 3 most recent
                break
            report += f"  - {memory['emotion'].capitalize()} ({memory['intensity']:.2f}): {memory['reason']}\n"
    
    # Total elapsed time
    hours = int(self.total_elapsed_time // 60)
    minutes = int(self.total_elapsed_time % 60)
    report += f"\nTotal simulation time: {hours}h {minutes}m\n"
    
    return report
import json
import re
from typing import Optional, Dict

# src/emotion_response.py
from typing import Optional

def process_input(self, input_text: str, elapsed_minutes: Optional[float] = None):
    """Process input text to update emotional state using config"""
    # Update emotions based on time elapsed
    self.update_emotional_state(elapsed_minutes)
    
    # Get trigger settings from config
    trigger_settings = self.personality_config["emotion_trigger_settings"]
    
    # Simple keyword-based sentiment analysis
    input_lower = input_text.lower()
    
    # Get emotion keywords from config
    for emotion, config in self.personality_config["emotions"].items():
        keywords = config["keywords"]
        for keyword in keywords:
            if keyword in input_lower:
                # Determine intensity based on position and emphasis
                base_intensity = trigger_settings["base_intensity"]
                
                # Detect emphasis (exclamation marks, ALL CAPS, repetition)
                if "!" in input_text:
                    base_intensity += trigger_settings["exclamation_bonus"]
                if keyword.upper() in input_text:
                    base_intensity += trigger_settings["caps_bonus"]
                if input_lower.count(keyword) > 1:
                    base_intensity += trigger_settings["repetition_bonus"]
                    
                self.trigger_emotion(emotion, base_intensity, f"Detected '{keyword}' in input")

def trigger_emotion(self, emotion: str, intensity: float, reason: Optional[str] = None):
    """Trigger a specific emotion with given intensity"""
    if emotion not in self.emotional_state.emotions:
        return False
        
    # Apply personality-based reactivity
    reactivity = self.emotional_state.personality["reactivity"]
    current = self.emotional_state.emotions[emotion]
    target = current + (intensity * reactivity)
    
    # Update the emotion
    self.emotional_state.emotions[emotion] = max(0.0, min(1.0, target))
    
    # Record significant emotional events
    if abs(target - current) > 0.2:
        self._add_to_memory(emotion, intensity, reason)
    
    # Apply emotional contagion
    self._apply_emotional_contagion(emotion)
    
    # Update dimensions
    self._update_dimensions()
    
    return True

def apply_emotional_contagion(self, source_emotion: str):
    """Apply emotional contagion effects (emotions affecting other emotions)"""
    if source_emotion not in self.emotion_relationships:
        return
    
    contagion_strength = self.emotional_state.personality["emotional_contagion"]
    source_intensity = self.emotional_state.emotions[source_emotion]
    
    # Get minimum intensity from config
    min_intensity = self.personality_config["contagion_settings"]["minimum_intensity"]
    
    # Only significant emotions cause contagion
    if source_intensity < min_intensity:
        return
        
    # Apply influence to related emotions
    for target_emotion, influence in self.emotion_relationships[source_emotion].items():
        # Calculate effect based on source intensity and relationship strength
        effect = source_intensity * influence * contagion_strength
        
        # Apply the effect
        current = self.emotional_state.emotions[target_emotion]
        self.emotional_state.emotions[target_emotion] = max(0.0, min(1.0, current + effect))

def generate_emotion_analysis_prompt(self, text_to_analyze: str) -> str:
    """
    Generate a prompt for an LLM to analyze emotions in the given text
    
    Args:
        text_to_analyze: The text to analyze for emotional content
        
    Returns:
        A formatted prompt string to send to an LLM
    """
    # Get the list of emotions we want to analyze
    target_emotions = list(self.emotional_state.emotions.keys())
    emotions_list = ", ".join(target_emotions)
    
    prompt = f"""Analyze the emotional content of this text and provide confidence scores (0.0 to 1.0) 
    for each of these emotions: {emotions_list}.
    
    Text to analyze: "{text_to_analyze}"
    
    Return your answer as a JSON object with emotions as keys and confidence scores as values.
    For example: {{"joy": 0.8, "sadness": 0.1}}
    
    JSON response:"""
    
    return prompt

def process_emotion_analysis(self, analysis_result: str) -> bool:
    """Process the emotion analysis result from an LLM and update Himalia's emotional state"""
    # Track if we processed anything successfully
    processed_any = False
    
    try:
        # First try to parse the whole response as JSON
        try:
            emotion_scores = json.loads(analysis_result)
            if isinstance(emotion_scores, dict):
                processed_any = self._apply_emotion_scores(emotion_scores)
                return processed_any
        except json.JSONDecodeError:
            # Not valid JSON, continue to regex extraction
            pass
        
        # Try to extract JSON using regex
        json_match = re.search(r'\{.*\}', analysis_result, re.DOTALL)
        if json_match:
            try:
                json_str = json_match.group(0)
                emotion_scores = json.loads(json_str)
                if isinstance(emotion_scores, dict):
                    processed_any = self._apply_emotion_scores(emotion_scores)
            except json.JSONDecodeError:
                pass
                
        # If we still haven't found valid JSON, look for key-value pairs
        if not processed_any:
            # Look for patterns like "joy: 0.8" or "joy = 0.8"
            pattern = r'(\w+)[\s]*[=:]+[\s]*(0\.\d+|1\.0|1)'
            matches = re.findall(pattern, analysis_result)
            
            if matches:
                extracted_scores = {}
                for emotion, score in matches:
                    if emotion in self.emotional_state.emotions:
                        extracted_scores[emotion] = float(score)
                
                if extracted_scores:
                    processed_any = self._apply_emotion_scores(extracted_scores)
        
        return processed_any
    except Exception as e:
        print(f"Error processing LLM emotion analysis: {e}")
        return False

def _apply_emotion_scores(self, emotion_scores: Dict[str, float]) -> bool:
    """Apply extracted emotion scores to the emotional state"""
    # Get emotion trigger settings
    trigger_settings = self.personality_config.get("llm_analysis_settings", {})
    threshold = trigger_settings.get("confidence_threshold", 0.3)
    
    processed_any = False
    
    # Trigger emotions based on the scores
    for emotion, score in emotion_scores.items():
        # Convert score to float if it's a string
        if isinstance(score, str):
            try:
                score = float(score)
            except ValueError:
                continue
                
        if emotion in self.emotional_state.emotions and score > threshold:
            self.trigger_emotion(emotion, float(score), f"LLM detected {emotion} ({score:.2f})")
            processed_any = True
    
    return processed_any
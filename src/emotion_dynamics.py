# src/emotion_dynamics.py
import datetime
import random
from typing import Optional

def update_emotional_state(self, elapsed_minutes: Optional[float] = None):
    """Update emotional state based on time elapsed"""
    now = datetime.datetime.now()
    
    # Calculate time passed since last update (in minutes)
    if elapsed_minutes is not None:
        # Use provided simulation time
        time_delta = elapsed_minutes
    else:
        # Use real time
        time_delta = (now - self.last_update).total_seconds() / 60.0
    
    self.total_elapsed_time += time_delta
    
    # Apply natural decay
    self._apply_emotional_decay(time_delta)
    
    # Apply random fluctuations
    self._apply_random_fluctuations(time_delta)
    
    # Update dimensions based on current emotions
    self._update_dimensions()
    
    self.last_update = now
    
    return time_delta

def apply_emotional_decay(self, elapsed_minutes: float):
    """Emotions naturally decay toward baseline over time"""
    decay_factor = min(1.0, self.emotional_state.personality["decay_rate"] * elapsed_minutes)
    
    for emotion, current in self.emotional_state.emotions.items():
        # Get baseline from personality config
        target = self.personality_config["emotions"][emotion]["baseline"]
        
        # Apply decay
        self.emotional_state.emotions[emotion] = current + (target - current) * decay_factor

def apply_random_fluctuations(self, elapsed_minutes: float):
    """Apply small random changes to emotions based on volatility"""
    volatility = self.emotional_state.personality["volatility"]
    volatility_settings = self.personality_config["volatility_settings"]
    fluctuation_chance = min(0.9, volatility * elapsed_minutes * 
                            volatility_settings["fluctuation_chance_multiplier"])
    
    # Only apply fluctuations occasionally
    if random.random() < fluctuation_chance:
        # Pick a random emotion to fluctuate
        emotion = random.choice(list(self.emotional_state.emotions.keys()))
        
        # Generate a small random change
        change = (random.random() -
                 0.5) * volatility * volatility_settings["change_magnitude"]
        
        # Apply the change
        current = self.emotional_state.emotions[emotion]
        self.emotional_state.emotions[emotion] = max(0.0, min(1.0, current + change))
        
        # If significant enough, record in memory
        if abs(change) > volatility_settings["significance_threshold"]:
            self._add_to_memory(emotion, abs(change), "Random mood shift")

def update_dimensions(self):
    """Update dimensions based on emotion values using config settings"""
    emotions = self.emotional_state.emotions
    
    # Reset all dimensions to baseline values
    for dim_name, dim_config in self.personality_config["dimensions"].items():
        self.emotional_state.dimensions[dim_name] = dim_config["baseline"]
    
    # Apply each emotion's influence on dimensions
    for emotion_name, intensity in emotions.items():
        if intensity > 0.0:  # Only apply if emotion has some intensity
            emotion_config = self.personality_config["emotions"][emotion_name]
            for dim_name, influence in emotion_config["dimension_influences"].items():
                self.emotional_state.dimensions[dim_name] += intensity * influence
    
    # Normalize dimensions to -1.0 to 1.0 range
    for dim in self.emotional_state.dimensions:
        self.emotional_state.dimensions[dim] = max(-1.0, min(1.0, 
                                                self.emotional_state.dimensions[dim]))
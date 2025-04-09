# src/emotional_state.py
import datetime
import random
from typing import Dict, Any

class EmotionalState:
    """Represents the emotional state of the system"""
    
    def __init__(self, personality_config: Dict[str, Any] = None):
        """Initialize emotional state from personality config"""
        if personality_config is None:
            raise ValueError("Personality configuration is required")
            
        # Initialize dimensions from config
        self.dimensions = {}
        for dim_name, dim_config in personality_config["dimensions"].items():
            self.dimensions[dim_name] = dim_config["baseline"]
        
        # Initialize emotions from config with random variations
        self.emotions = {}
        volatility = personality_config["personality_traits"]["volatility"]
        
        for emotion_name, emotion_config in personality_config["emotions"].items():
            baseline = emotion_config["baseline"]
            
            # Calculate randomization range based on volatility and baseline
            # Higher baselines get more positive random variations
            # Higher volatility means larger possible variations
            # Higher baseline = bias toward positive variations
            variation_range = volatility * 0.5  # Max variation is 50% of volatility
            
            # Bias toward positive variations if baseline is higher
            # (more likely to start above baseline than below it)
            positive_bias = baseline * 0.5
            
            # Calculate random variation
            random_adjustment = random.uniform(
                -variation_range * (1.0 - positive_bias),  # Lower bound (reduced for high baselines)
                variation_range * (1.0 + positive_bias)    # Upper bound (increased for high baselines)
            )
            
            # Apply the adjustment and clamp to valid range
            initial_value = max(0.0, min(1.0, baseline + random_adjustment))
            self.emotions[emotion_name] = initial_value
        
        # Initialize personality traits from config
        self.personality = {}
        for trait_name, trait_value in personality_config["personality_traits"].items():
            self.personality[trait_name] = trait_value
        
        # Initialize emotional memory
        self.emotional_memory = []
        self.memory_capacity = personality_config["memory_capacity"]
        
        # Timestamp of last update
        self.last_update = datetime.datetime.now()
        
        # Record significant initial variations as memories
        for emotion_name, value in self.emotions.items():
            baseline = personality_config["emotions"][emotion_name]["baseline"]
            if abs(value - baseline) > 0.15:  # Significant deviation from baseline
                self.emotional_memory.append({
                    "emotion": emotion_name,
                    "intensity": abs(value - baseline),
                    "reason": "Initial mood variation",
                    "timestamp": self.last_update,
                    "elapsed_time": 0.0
                })
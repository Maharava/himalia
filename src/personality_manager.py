import json
import os
from typing import Dict, List, Any, Optional

class PersonalityManager:
    """Manages personality configurations for Himalia"""
    
    REQUIRED_DIMENSIONS = ["pleasure", "arousal", "dominance", "intimacy"]
    REQUIRED_EMOTIONS = ["joy", "sadness", "anger", "fear", "trust", "disgust", 
                         "anticipation", "surprise", "curiosity", "libido"]
    
    def __init__(self, personality_dir: str = "personalities"):
        """Initialize the personality manager"""
        self.personality_dir = personality_dir
        self.loaded_personality = None
        
    def get_available_personalities(self) -> List[str]:
        """Get a list of available personality files"""
        if not os.path.exists(self.personality_dir):
            os.makedirs(self.personality_dir)
            
        return [f for f in os.listdir(self.personality_dir) 
                if f.endswith('.json')]
    
    def load_personality(self, filename: str) -> Dict[str, Any]:
        """Load a personality configuration from file"""
        filepath = os.path.join(self.personality_dir, filename)
        
        try:
            with open(filepath, 'r') as f:
                personality = json.load(f)
                
            # Validate the personality configuration
            self._validate_personality(personality)
            
            self.loaded_personality = personality
            return personality
            
        except Exception as e:
            raise Exception(f"Failed to load personality from {filepath}: {e}")
    
    def _validate_personality(self, personality: Dict[str, Any]) -> None:
        """Validate that a personality configuration has all required elements"""
        # Check dimensions
        if "dimensions" not in personality:
            raise ValueError("Personality is missing 'dimensions' section")
            
        for dim in self.REQUIRED_DIMENSIONS:
            if dim not in personality["dimensions"]:
                raise ValueError(f"Required dimension '{dim}' is missing")
        
        # Check emotions
        if "emotions" not in personality:
            raise ValueError("Personality is missing 'emotions' section")
            
        for emotion in self.REQUIRED_EMOTIONS:
            if emotion not in personality["emotions"]:
                raise ValueError(f"Required emotion '{emotion}' is missing")
                
        # Check each emotion has correct attributes
        for emotion, config in personality["emotions"].items():
            required_attributes = ["baseline", "keywords", "prompt_rules", 
                                  "relationships", "dimension_influences"]
            for attr in required_attributes:
                if attr not in config:
                    raise ValueError(f"Emotion '{emotion}' is missing '{attr}' attribute")
            
            # Ensure dimension_influences refers to valid dimensions
            for dim in config["dimension_influences"]:
                if dim not in personality["dimensions"]:
                    raise ValueError(f"Emotion '{emotion}' references undefined dimension '{dim}'")
                    
        # Check personality_traits
        if "personality_traits" not in personality:
            raise ValueError("Personality is missing 'personality_traits' section")
            
        required_traits = ["baseline_mood", "reactivity", "decay_rate", 
                          "volatility", "emotional_contagion"]
        for trait in required_traits:
            if trait not in personality["personality_traits"]:
                raise ValueError(f"Required personality trait '{trait}' is missing")
                
        # Check memory_capacity is present
        if "memory_capacity" not in personality:
            raise ValueError("Personality is missing 'memory_capacity' setting")
    
    def save_personality(self, personality: Dict[str, Any], filename: str) -> None:
        """Save a personality configuration to file"""
        # Validate before saving
        self._validate_personality(personality)
        
        filepath = os.path.join(self.personality_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(personality, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save personality to {filepath}: {e}")
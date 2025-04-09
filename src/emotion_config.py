# src/emotion_config.py
import os
import json
import random
from typing import Dict, Optional
from src.emotional_state import EmotionalState
from src.personality_manager import PersonalityManager

def initialize_himalia(self, config_path: Optional[str] = None):
    """Initialize the Himalia system"""
    # Set up personality manager
    self.personality_manager = PersonalityManager()
    
    # Load personality configuration
    if config_path and os.path.exists(config_path):
        # Load custom personality
        personality_name = os.path.basename(config_path)
        self.personality_config = self.personality_manager.load_personality(personality_name)
    else:
        # Load default personality
        self.personality_config = self.personality_manager.load_personality("default.json")
    
    # Initialize emotional state with personality config
    self.emotional_state = EmotionalState(self.personality_config)
    self.last_update = self.emotional_state.last_update
    
    # Initialize random seed
    self.random_seed = random.randint(1, 10000)
    random.seed(self.random_seed)
    
    # Track total simulation time
    self.total_elapsed_time = 0.0  # minutes
    
    # Load custom configuration if provided
    if config_path and os.path.exists(config_path):
        self.load_config(config_path)
    
    # Initialize emotion relationships
    self.emotion_relationships = self._initialize_emotion_relationships()

def initialize_emotion_relationships(self) -> Dict[str, Dict[str, float]]:
    """Define how emotions influence each other from config"""
    relationships = {}
    
    # Extract relationship data from personality config
    for emotion_name, emotion_config in self.personality_config["emotions"].items():
        relationships[emotion_name] = emotion_config["relationships"]
    
    return relationships

def load_config(self, config_path: str):
    """Load configuration from a JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        # Update personality if specified
        if "personality" in config:
            for trait, value in config["personality"].items():
                if trait in self.emotional_state.personality:
                    self.emotional_state.personality[trait] = value
                    
        # Update initial emotions if specified
        if "initial_emotions" in config:
            for emotion, value in config["initial_emotions"].items():
                if emotion in self.emotional_state.emotions:
                    self.emotional_state.emotions[emotion] = value
                    
        # Update other configuration parameters as needed
        if "memory_capacity" in config:
            self.emotional_state.memory_capacity = config["memory_capacity"]
            
    except Exception as e:
        print(f"Error loading configuration: {e}")
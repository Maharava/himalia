# src/himalia.py
import datetime
import random
import os
from typing import Dict, Optional

from src.emotional_state import EmotionalState
from src.emotion_config import initialize_himalia, initialize_emotion_relationships, load_config
from src.emotion_dynamics import update_emotional_state, apply_emotional_decay, apply_random_fluctuations, update_dimensions
from src.emotion_response import process_input, trigger_emotion, apply_emotional_contagion
from src.emotion_memory import add_to_memory
from src.emotion_output import generate_prompt, get_status_report
from src.emotion_persistence import save_state, load_state

class Himalia:
    """Main emotion simulation system"""
    
    def __init__(self, config_path: Optional[str] = None):
        # Initialization from emotion_config
        self._initialize_himalia(config_path)
    
    # Import methods from different modules
    _initialize_himalia = initialize_himalia
    _initialize_emotion_relationships = initialize_emotion_relationships
    load_config = load_config
    
    update_emotional_state = update_emotional_state
    _apply_emotional_decay = apply_emotional_decay
    _apply_random_fluctuations = apply_random_fluctuations
    _update_dimensions = update_dimensions
    
    process_input = process_input
    trigger_emotion = trigger_emotion
    _apply_emotional_contagion = apply_emotional_contagion
    
    _add_to_memory = add_to_memory
    
    generate_prompt = generate_prompt
    get_status_report = get_status_report
    
    save_state = save_state
    load_state = load_state
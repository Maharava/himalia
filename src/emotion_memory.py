# src/emotion_memory.py
import datetime
from typing import Optional

def add_to_memory(self, emotion: str, intensity: float, reason: Optional[str] = None):
    """Add an emotional event to memory"""
    self.emotional_state.emotional_memory.append({
        "emotion": emotion,
        "intensity": intensity,
        "reason": reason if reason else "Unknown cause",
        "timestamp": datetime.datetime.now(),
        "elapsed_time": self.total_elapsed_time
    })
    
    # Maintain memory capacity
    if len(self.emotional_state.emotional_memory) > self.emotional_state.memory_capacity:
        self.emotional_state.emotional_memory.pop(0)
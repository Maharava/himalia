# src/emotion_persistence.py
import json
import datetime

def save_state(self, filepath: str):
    """Save current emotional state to a file"""
    state = {
        "dimensions": self.emotional_state.dimensions,
        "emotions": self.emotional_state.emotions,
        "personality": self.emotional_state.personality,
        "memory": self.emotional_state.emotional_memory,
        "total_elapsed_time": self.total_elapsed_time,
        "timestamp": str(datetime.datetime.now())
    }
    
    try:
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving state: {e}")
        return False

def load_state(self, filepath: str):
    """Load emotional state from a file"""
    try:
        with open(filepath, 'r') as f:
            state = json.load(f)
            
        self.emotional_state.dimensions = state["dimensions"]
        self.emotional_state.emotions = state["emotions"]
        self.emotional_state.personality = state["personality"]
        self.emotional_state.emotional_memory = state["memory"]
        self.total_elapsed_time = state["total_elapsed_time"]
        self.last_update = datetime.datetime.now()
        
        return True
    except Exception as e:
        print(f"Error loading state: {e}")
        return False
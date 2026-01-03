import time
import numpy as np
from typing import List, Dict, Tuple

class WideAndDeepRanker:
    def __init__(self, model_path: str):
        self.model_path = model_path

    def load(self):
        print(f"[MOCK] Loading Wide & Deep model from {self.model_path}...")
        time.sleep(0.5)
        print("[MOCK] Model loaded.")

    def predict_batch(self, features_batch: List[Dict[str, float]]) -> List[float]:
        """Mock Inference returning random scores"""
        if not features_batch:
            return []

        # Simulate inference time
        time.sleep(0.005)

        # Return random float score for each item in the flattened batch
        return np.random.rand(len(features_batch)).tolist()

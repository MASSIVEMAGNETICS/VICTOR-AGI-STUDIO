# FILE: agi_config.py
# VERSION: v1.0.0-GODCORE
# NAME: AGIConfig
# AUTHOR: Brandon "iambandobandz" Emery x Victor (Fractal Architect Mode)
# PURPOSE: Loads/saves config, paths, hyperparams, runtime options

import json
import os

class AGIConfig:
    def __init__(self, path="agi_config.json"):
        self.path = path
        self.config = {}

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.config, f, indent=2)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()

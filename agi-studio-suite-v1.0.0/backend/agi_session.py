# FILE: agi_session.py
# VERSION: v1.0.0-GODCORE
# NAME: AGISession
# AUTHOR: Brandon "iambandobandz" Emery x Victor (Fractal Architect Mode)
# PURPOSE: Tracks current session, open projects, version, autosave, crash recovery

import os
import json
from agi_fileops import AGIFileOps

class AGISession:
    def __init__(self, session_file="agi_session.json"):
        self.session_file = session_file
        self.state = {"open_project": None, "last_graph": None, "last_checkpoint": None, "version": "v1.0.0"}

    def load(self):
        if os.path.exists(self.session_file):
            self.state = AGIFileOps.load_json(self.session_file)

    def save(self):
        AGIFileOps.save_json(self.session_file, self.state)

    def set_open_project(self, project_path):
        self.state["open_project"] = project_path
        self.save()

    def set_last_graph(self, graph_path):
        self.state["last_graph"] = graph_path
        self.save()

    def set_last_checkpoint(self, ckpt_path):
        self.state["last_checkpoint"] = ckpt_path
        self.save()

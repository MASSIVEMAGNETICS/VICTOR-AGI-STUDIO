# FILE: agi_fileops.py
# VERSION: v1.0.0-GODCORE
# NAME: AGIFileOps
# AUTHOR: Brandon "iambandobandz" Emery x Victor (Fractal Architect Mode)
# PURPOSE: Robust, fail-proof, local-only file handling for all model data

import json
import os
import shutil

class AGIFileOps:
    @staticmethod
    def save_json(path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load_json(path):
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def backup_file(src_path, backup_dir="backups"):
        os.makedirs(backup_dir, exist_ok=True)
        base = os.path.basename(src_path)
        ts = AGIFileOps._timestamp()
        dst = os.path.join(backup_dir, f"{base}.{ts}.bak")
        shutil.copy2(src_path, dst)
        return dst

    @staticmethod
    def autosave(path, data, key="autosave"):
        d = {"data": data, "key": key, "ts": AGIFileOps._timestamp()}
        AGIFileOps.save_json(path, d)

    @staticmethod
    def export_bundle(bundle_name, files):
        os.makedirs("exports", exist_ok=True)
        bundle_path = os.path.join("exports", bundle_name)
        with open(bundle_path, "w") as f:
            for fp in files:
                f.write(f"\n--- {fp} ---\n")
                with open(fp, "r") as f2:
                    f.write(f2.read())
        return bundle_path

    @staticmethod
    def _timestamp():
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")

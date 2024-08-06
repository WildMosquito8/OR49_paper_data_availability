import json

class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, "r") as file:
                config = json.load(file)
            return config
        except FileNotFoundError:
            raise ValueError(f"Configuration file not found: {self.config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from the configuration file: {self.config_path}")

    def get(self, key, default=None):
        return self.config.get(key, default)

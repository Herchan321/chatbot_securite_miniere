import logging
from datetime import datetime
import json

class ChatbotMonitor:
    def __init__(self, log_file="logs/chatbot.log"):
        self.log_file = log_file
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def log_interaction(self, question: str, answer: str, sources: list):
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "sources": sources
        }
        logging.info(f"Interaction: {json.dumps(interaction)}")
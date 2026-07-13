import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        """Initialize FinBERT model for financial sentiment analysis"""
        try:
            self.model_name = "ProsusAI/finbert"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"FinBERT loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Error loading FinBERT model: {e}")
            raise

    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment of financial text
        
        Args:
            text: Financial headline or news snippet
            
        Returns:
            {
                "sentiment": "positive" | "negative" | "neutral",
                "score": 0.0-1.0,
                "confidence": 0.0-1.0
            }
        """
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            inputs = {key: val.to(self.device) for key, val in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=-1)
            
            # FinBERT labels: 0=positive, 1=negative, 2=neutral
            label_map = {0: "positive", 1: "negative", 2: "neutral"}
            pred_label = torch.argmax(probs, dim=-1).item()
            sentiment = label_map[pred_label]
            confidence = probs[0][pred_label].item()
            
            # Convert to 0-1 score where 1 is most positive
            if sentiment == "positive":
                score = confidence
            elif sentiment == "negative":
                score = 1 - confidence
            else:
                score = 0.5
            
            return {
                "sentiment": sentiment,
                "score": round(score, 3),
                "confidence": round(confidence, 3)
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {"sentiment": "neutral", "score": 0.5, "confidence": 0.0}
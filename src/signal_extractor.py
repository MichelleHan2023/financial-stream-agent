import re
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class SignalExtractor:
    def __init__(self):
        """Initialize signal extractor without spaCy"""
        # Guidance direction keywords
        self.raise_keywords = ["raises", "raised", "raises guidance", "boosts", "upbeat", "strong", "exceeds", "beat", "beats"]
        self.lower_keywords = ["lowers", "lowered", "cuts", "misses", "missed", "disappoints", "weak", "declines", "down"]
        self.maintain_keywords = ["maintains", "reaffirms", "confirms", "in line with"]
        
    def extract_ticker(self, text: str) -> Optional[str]:
        """
        Extract stock ticker from headline using regex
        
        Args:
            text: Headline text
            
        Returns:
            Ticker symbol (e.g., "AAPL") or None
        """
        # Try regex patterns: $TICKER or (TICKER)
        regex_patterns = [
            r'\$([A-Z]{1,5})',           # $AAPL
            r'\(([A-Z]{1,5})\)',          # (AAPL)
            r'ticker\s+([A-Z]{1,5})',     # ticker AAPL
        ]
        
        for pattern in regex_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).upper()
        
        # Try company name to ticker mapping
        company_map = {
            "Apple": "AAPL",
            "Microsoft": "MSFT",
            "Google": "GOOGL",
            "Alphabet": "GOOGL",
            "Amazon": "AMZN",
            "Tesla": "TSLA",
            "Meta": "META",
            "Facebook": "META",
            "Nvidia": "NVDA",
            "Intel": "INTC",
            "AMD": "AMD",
            "Netflix": "NFLX",
            "Spotify": "SPOT",
        }
        
        for company, ticker in company_map.items():
            if company.lower() in text.lower():
                return ticker
        
        return None
    
    def extract_guidance_direction(self, text: str) -> Dict[str, any]:
        """
        Determine if guidance is being raised, lowered, or maintained
        
        Args:
            text: Headline text
            
        Returns:
            {
                "direction": "raised" | "lowered" | "maintained" | "unknown",
                "confidence": 0.0-1.0
            }
        """
        text_lower = text.lower()
        
        # Check raise keywords
        raise_count = sum(1 for kw in self.raise_keywords if kw in text_lower)
        lower_count = sum(1 for kw in self.lower_keywords if kw in text_lower)
        maintain_count = sum(1 for kw in self.maintain_keywords if kw in text_lower)
        
        if raise_count > lower_count and raise_count > maintain_count:
            return {"direction": "raised", "confidence": min(raise_count * 0.3, 1.0)}
        elif lower_count > raise_count and lower_count > maintain_count:
            return {"direction": "lowered", "confidence": min(lower_count * 0.3, 1.0)}
        elif maintain_count > 0:
            return {"direction": "maintained", "confidence": min(maintain_count * 0.3, 1.0)}
        else:
            return {"direction": "unknown", "confidence": 0.0}
    
    def extract_signals(self, headline: str, sentiment_score: float) -> Dict:
        """
        Extract all signals from a headline
        
        Args:
            headline: Financial headline
            sentiment_score: Sentiment score from analyzer (0-1)
            
        Returns:
            {
                "ticker": "AAPL",
                "guidance_direction": "raised",
                "guidance_confidence": 0.8,
                "sentiment_score": 0.85,
                "headline": "..."
            }
        """
        ticker = self.extract_ticker(headline)
        guidance = self.extract_guidance_direction(headline)
        
        return {
            "ticker": ticker,
            "guidance_direction": guidance["direction"],
            "guidance_confidence": guidance["confidence"],
            "sentiment_score": sentiment_score,
            "headline": headline
        }
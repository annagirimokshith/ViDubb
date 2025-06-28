import os
import re
import logging
from groq import Groq
import requests
import json
from typing import Optional, Dict, Any

class TranslationService:
    def __init__(self, groq_api_key: str = None, openrouter_api_key: str = None):
        """
        Initialize translation service with multiple providers
        
        Args:
            groq_api_key: Groq API key
            openrouter_api_key: OpenRouter API key
        """
        self.groq_client = None
        self.openrouter_api_key = openrouter_api_key
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        
        # Initialize Groq client
        if groq_api_key:
            try:
                self.groq_client = Groq(api_key=groq_api_key)
                logging.info("Groq client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Groq client: {e}")
        
        # Validate OpenRouter API key
        if openrouter_api_key:
            if self._validate_openrouter_key():
                logging.info("OpenRouter API key validated successfully")
            else:
                logging.warning("OpenRouter API key validation failed")
                self.openrouter_api_key = None
    
    def _validate_openrouter_key(self) -> bool:
        """Validate OpenRouter API key"""
        try:
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get(f"{self.openrouter_base_url}/models", headers=headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logging.error(f"OpenRouter key validation error: {e}")
            return False
    
    def translate_with_groq(self, sentence: str, before_context: str, after_context: str, 
                           target_language: str, model: str = "llama3-70b-8192") -> Optional[str]:
        """
        Translate using Groq API
        
        Args:
            sentence: Text to translate
            before_context: Previous sentence for context
            after_context: Next sentence for context
            target_language: Target language
            model: Groq model to use
            
        Returns:
            Translated text or None if failed
        """
        if not self.groq_client:
            return None
        
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        Role: You are a professional translator who translates concisely in short sentences while preserving meaning and context.
                        
                        Instruction:
                        Translate the given sentence into {target_language}. Consider the context provided by the previous and next sentences.
                        
                        Previous context: {before_context}
                        Sentence to translate: {sentence}
                        Next context: {after_context}
                        
                        Output format:
                        [[sentence translation: <your translation>]]
                        """,
                    }
                ],
                model=model,
                temperature=0.3,
                max_tokens=500
            )
            
            # Extract translation using regex
            pattern = r'\[\[sentence translation: (.*?)\]\]'
            match = re.search(pattern, chat_completion.choices[0].message.content, re.DOTALL)
            
            if match:
                return match.group(1).strip()
            else:
                # Fallback: return the full response if pattern doesn't match
                return chat_completion.choices[0].message.content.strip()
                
        except Exception as e:
            logging.error(f"Groq translation error: {e}")
            return None
    
    def translate_with_openrouter(self, sentence: str, before_context: str, after_context: str,
                                 target_language: str, model: str = "anthropic/claude-3.5-sonnet") -> Optional[str]:
        """
        Translate using OpenRouter API
        
        Args:
            sentence: Text to translate
            before_context: Previous sentence for context
            after_context: Next sentence for context
            target_language: Target language
            model: OpenRouter model to use
            
        Returns:
            Translated text or None if failed
        """
        if not self.openrouter_api_key:
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://vidubb.ai",
                "X-Title": "ViDubb Translation Service"
            }
            
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
                        Role: You are a professional translator specializing in video dubbing and subtitle translation.
                        
                        Task: Translate the given sentence into {target_language} while maintaining:
                        - Natural flow and timing suitable for video dubbing
                        - Emotional tone and context
                        - Cultural appropriateness
                        
                        Context:
                        Previous: {before_context}
                        Current: {sentence}
                        Next: {after_context}
                        
                        Provide only the translation without explanations.
                        """
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }
            
            response = requests.post(
                f"{self.openrouter_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                logging.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logging.error(f"OpenRouter translation error: {e}")
            return None
    
    def translate(self, sentence: str, before_context: str = "", after_context: str = "",
                 target_language: str = "English", provider: str = "auto") -> Optional[str]:
        """
        Translate text using the best available provider
        
        Args:
            sentence: Text to translate
            before_context: Previous sentence for context
            after_context: Next sentence for context
            target_language: Target language
            provider: Preferred provider ("groq", "openrouter", "auto")
            
        Returns:
            Translated text or None if all providers fail
        """
        if provider == "groq" and self.groq_client:
            return self.translate_with_groq(sentence, before_context, after_context, target_language)
        elif provider == "openrouter" and self.openrouter_api_key:
            return self.translate_with_openrouter(sentence, before_context, after_context, target_language)
        elif provider == "auto":
            # Try OpenRouter first (generally higher quality), then Groq
            if self.openrouter_api_key:
                result = self.translate_with_openrouter(sentence, before_context, after_context, target_language)
                if result:
                    return result
            
            if self.groq_client:
                result = self.translate_with_groq(sentence, before_context, after_context, target_language)
                if result:
                    return result
        
        logging.error("No translation providers available or all failed")
        return None
    
    def get_available_providers(self) -> Dict[str, bool]:
        """Get status of available translation providers"""
        return {
            "groq": self.groq_client is not None,
            "openrouter": self.openrouter_api_key is not None
        }
    
    def get_recommended_models(self) -> Dict[str, list]:
        """Get recommended models for each provider"""
        return {
            "groq": [
                "llama3-70b-8192",
                "llama3-8b-8192",
                "mixtral-8x7b-32768"
            ],
            "openrouter": [
                "anthropic/claude-3.5-sonnet",
                "openai/gpt-4o",
                "google/gemini-pro-1.5",
                "meta-llama/llama-3.1-70b-instruct"
            ]
        }

def setup_translation_service() -> TranslationService:
    """
    Setup translation service with API keys from environment
    
    Returns:
        Configured TranslationService instance
    """
    from dotenv import load_dotenv
    load_dotenv()
    
    groq_api_key = os.getenv('GROQ_TOKEN') or os.getenv('Groq_TOKEN')
    openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not groq_api_key and not openrouter_api_key:
        logging.warning("No translation API keys found. Translation will use fallback methods.")
    
    return TranslationService(groq_api_key, openrouter_api_key)
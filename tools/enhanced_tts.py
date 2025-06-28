import os
import logging
from TTS.api import TTS
from pydub import AudioSegment
from .google_tts import GoogleTTS, get_google_language_code

class EnhancedTTS:
    def __init__(self, use_google_tts=False, google_credentials_path=None):
        """
        Enhanced TTS system that can use either Coqui TTS or Google Cloud TTS
        
        Args:
            use_google_tts: Whether to use Google Cloud TTS as primary
            google_credentials_path: Path to Google Cloud credentials JSON
        """
        self.use_google_tts = use_google_tts
        self.google_tts = None
        self.coqui_tts = None
        
        # Initialize Google TTS if requested
        if use_google_tts:
            self.google_tts = GoogleTTS(google_credentials_path)
            if not self.google_tts.available:
                logging.warning("Google TTS not available, falling back to Coqui TTS")
                self.use_google_tts = False
        
        # Initialize Coqui TTS as fallback or primary
        if not self.use_google_tts or not self.google_tts or not self.google_tts.available:
            try:
                os.environ["COQUI_TOS_AGREED"] = "1"
                device = "cuda" if os.system("nvidia-smi") == 0 else "cpu"
                self.coqui_tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=(device == "cuda"))
                logging.info("Coqui TTS initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Coqui TTS: {e}")
    
    def synthesize_speech(self, text, language_code, speaker_wav=None, emotion=None, 
                         speed=1.0, output_path=None, voice_name=None, gender=None):
        """
        Synthesize speech using the configured TTS system
        
        Args:
            text: Text to synthesize
            language_code: Language code
            speaker_wav: Path to speaker reference audio (for Coqui TTS)
            emotion: Emotion for synthesis (for Coqui TTS)
            speed: Speaking speed
            output_path: Path to save the audio file
            voice_name: Voice name (for Google TTS)
            gender: Voice gender (for Google TTS)
            
        Returns:
            AudioSegment object or path to generated file
        """
        if self.use_google_tts and self.google_tts and self.google_tts.available:
            return self._synthesize_with_google(
                text, language_code, speed, output_path, voice_name, gender
            )
        elif self.coqui_tts:
            return self._synthesize_with_coqui(
                text, language_code, speaker_wav, emotion, speed, output_path
            )
        else:
            logging.error("No TTS system available")
            return None
    
    def _synthesize_with_google(self, text, language_code, speed, output_path, voice_name, gender):
        """Synthesize using Google Cloud TTS"""
        google_lang_code = get_google_language_code(language_code)
        
        if output_path:
            success = self.google_tts.synthesize_to_file(
                text=text,
                output_path=output_path,
                language_code=google_lang_code,
                voice_name=voice_name,
                gender=gender,
                speaking_rate=speed
            )
            return output_path if success else None
        else:
            return self.google_tts.synthesize_speech(
                text=text,
                language_code=google_lang_code,
                voice_name=voice_name,
                gender=gender,
                speaking_rate=speed
            )
    
    def _synthesize_with_coqui(self, text, language_code, speaker_wav, emotion, speed, output_path):
        """Synthesize using Coqui TTS"""
        try:
            if output_path:
                self.coqui_tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker_wav=speaker_wav,
                    language=language_code,
                    emotion=emotion,
                    speed=speed
                )
                return output_path
            else:
                # For in-memory synthesis, we need to use a temporary file
                import tempfile
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                    self.coqui_tts.tts_to_file(
                        text=text,
                        file_path=tmp_file.name,
                        speaker_wav=speaker_wav,
                        language=language_code,
                        emotion=emotion,
                        speed=speed
                    )
                    audio_segment = AudioSegment.from_wav(tmp_file.name)
                    os.unlink(tmp_file.name)  # Clean up temp file
                    return audio_segment
        except Exception as e:
            logging.error(f"Error with Coqui TTS synthesis: {e}")
            return None
    
    def get_available_voices(self, language_code):
        """Get available voices for the current TTS system"""
        if self.use_google_tts and self.google_tts and self.google_tts.available:
            google_lang_code = get_google_language_code(language_code)
            return self.google_tts.get_available_voices(google_lang_code)
        else:
            # Coqui TTS uses speaker reference files, so return empty list
            return []
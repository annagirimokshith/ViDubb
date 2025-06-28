import os
import io
from google.cloud import texttospeech
from pydub import AudioSegment
import tempfile
import logging

class GoogleTTS:
    def __init__(self, credentials_path=None):
        """
        Initialize Google Cloud TTS client
        
        Args:
            credentials_path: Path to Google Cloud service account JSON file
                            If None, will use GOOGLE_APPLICATION_CREDENTIALS env var
        """
        if credentials_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        
        try:
            self.client = texttospeech.TextToSpeechClient()
            self.available = True
            logging.info("Google Cloud TTS initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Google Cloud TTS: {e}")
            self.available = False
    
    def get_available_voices(self, language_code="en-US"):
        """
        Get available voices for a specific language
        
        Args:
            language_code: Language code (e.g., 'en-US', 'fr-FR', 'es-ES')
            
        Returns:
            List of available voice names
        """
        if not self.available:
            return []
        
        try:
            voices = self.client.list_voices()
            available_voices = []
            
            for voice in voices.voices:
                if language_code in voice.language_codes:
                    available_voices.append({
                        'name': voice.name,
                        'gender': voice.ssml_gender.name,
                        'language_codes': list(voice.language_codes)
                    })
            
            return available_voices
        except Exception as e:
            logging.error(f"Error getting available voices: {e}")
            return []
    
    def synthesize_speech(self, text, language_code="en-US", voice_name=None, 
                         gender=None, speaking_rate=1.0, pitch=0.0):
        """
        Synthesize speech using Google Cloud TTS
        
        Args:
            text: Text to synthesize
            language_code: Language code (e.g., 'en-US', 'fr-FR')
            voice_name: Specific voice name (optional)
            gender: Voice gender ('MALE', 'FEMALE', 'NEUTRAL') (optional)
            speaking_rate: Speaking rate (0.25 to 4.0)
            pitch: Voice pitch (-20.0 to 20.0)
            
        Returns:
            AudioSegment object or None if failed
        """
        if not self.available:
            logging.error("Google Cloud TTS not available")
            return None
        
        try:
            # Set up the text input
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Configure voice parameters
            voice_params = {
                'language_code': language_code
            }
            
            if voice_name:
                voice_params['name'] = voice_name
            elif gender:
                if gender.upper() == 'MALE':
                    voice_params['ssml_gender'] = texttospeech.SsmlVoiceGender.MALE
                elif gender.upper() == 'FEMALE':
                    voice_params['ssml_gender'] = texttospeech.SsmlVoiceGender.FEMALE
                else:
                    voice_params['ssml_gender'] = texttospeech.SsmlVoiceGender.NEUTRAL
            
            voice = texttospeech.VoiceSelectionParams(**voice_params)
            
            # Configure audio output
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=speaking_rate,
                pitch=pitch
            )
            
            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Convert to AudioSegment
            audio_content = io.BytesIO(response.audio_content)
            audio_segment = AudioSegment.from_mp3(audio_content)
            
            return audio_segment
            
        except Exception as e:
            logging.error(f"Error synthesizing speech: {e}")
            return None
    
    def synthesize_to_file(self, text, output_path, language_code="en-US", 
                          voice_name=None, gender=None, speaking_rate=1.0, pitch=0.0):
        """
        Synthesize speech and save to file
        
        Args:
            text: Text to synthesize
            output_path: Path to save the audio file
            language_code: Language code
            voice_name: Specific voice name (optional)
            gender: Voice gender (optional)
            speaking_rate: Speaking rate
            pitch: Voice pitch
            
        Returns:
            True if successful, False otherwise
        """
        audio_segment = self.synthesize_speech(
            text, language_code, voice_name, gender, speaking_rate, pitch
        )
        
        if audio_segment:
            try:
                audio_segment.export(output_path, format="wav")
                return True
            except Exception as e:
                logging.error(f"Error saving audio file: {e}")
                return False
        
        return False

# Language code mapping for Google Cloud TTS
GOOGLE_TTS_LANGUAGE_MAPPING = {
    'en': 'en-US',
    'es': 'es-ES', 
    'fr': 'fr-FR',
    'de': 'de-DE',
    'it': 'it-IT',
    'tr': 'tr-TR',
    'ru': 'ru-RU',
    'nl': 'nl-NL',
    'cs': 'cs-CZ',
    'ar': 'ar-XA',
    'zh-cn': 'zh-CN',
    'ja': 'ja-JP',
    'ko': 'ko-KR',
    'hi': 'hi-IN',
    'hu': 'hu-HU'
}

def get_google_language_code(vidubb_language_code):
    """
    Convert ViDubb language code to Google Cloud TTS language code
    
    Args:
        vidubb_language_code: Language code used in ViDubb
        
    Returns:
        Google Cloud TTS compatible language code
    """
    return GOOGLE_TTS_LANGUAGE_MAPPING.get(vidubb_language_code, 'en-US')
<div align="center">




<p align="center"><img src="images/Vidubb_img.png" width="1200" height="290" alt="Video dubbing">
   
# ViDubb: Free AI Dubbing/Translation with Voice and Emotion Cloning, Multilingual Support, and Lip-Sync
    
</div>
<div align="center">
    
|Kaggle|Gradio|Youtube|
|:-------:|:-------:|:-------:|
|[![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/medahmedkrichen/vidubb-kaggle-notebook)|[![Gradio](https://img.shields.io/badge/gradio-web_app-blue)](https://github.com/gradio-app/gradio)|[![Youtube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://www.youtube.com/@medahmedkrichen)|
|Free memory and GPU time!|Gradio Web App|Subscribe!|
  
</div>

 




## Video Dubbing with AI Cloning, Multilingual Capabilities, and Lip-Sync

ViDubb is an advanced AI-powered video dubbing solution focused on delivering high-quality, efficient dubbing for multilingual content. By utilizing cutting-edge voice cloning technology, ViDubb generates realistic voiceovers in multiple languages with exceptional accuracy. The system ensures perfect lip-sync synchronization, matching the voiceovers to the actors' movements, providing a seamless viewing experience. This approach not only enhances the natural flow of dialogue but also preserves the authenticity of the original video. ViDubb streamlines the dubbing process, enabling faster turnaround times while maintaining top-tier audio and visual quality for global audiences ( AI video dubbing / dubber).

---

## New Features

### 🎤 Google Cloud Text-to-Speech Integration

ViDubb now supports Google Cloud Text-to-Speech (TTS) for even higher quality voice synthesis:

- **Premium Voice Quality**: Access to Google's state-of-the-art neural voices
- **Multiple Voice Options**: Choose from various voice types and genders
- **Enhanced Language Support**: Better pronunciation and naturalness across languages
- **Fallback System**: Automatically falls back to Coqui TTS if Google Cloud is not configured

#### Setting up Google Cloud TTS

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Text-to-Speech API

2. **Create Service Account Credentials**:
   - Navigate to "IAM & Admin" > "Service Accounts"
   - Create a new service account
   - Download the JSON credentials file

3. **Configure ViDubb**:
   - Place your credentials JSON file in the project directory
   - Set the environment variable in your `.env` file:
     ```
     GOOGLE_CLOUD_CREDENTIALS_PATH=path/to/your/credentials.json
     USE_GOOGLE_TTS=true
     ```

4. **Enable in Interface**:
   - Check the "Use Google Cloud TTS" option in the Gradio interface

### 🌐 Enhanced Translation with OpenRouter + Groq

ViDubb now features advanced translation capabilities with multiple AI providers:

- **OpenRouter Integration**: Access to premium models like Claude 3.5 Sonnet, GPT-4, and Gemini Pro
- **Groq Support**: Fast inference with Llama 3 models
- **Automatic Fallback**: Intelligent provider selection for best results
- **Context-Aware Translation**: Better accuracy with sentence context

#### Setting up Translation APIs

1. **OpenRouter API** (Premium):
   - Sign up at [OpenRouter](https://openrouter.ai/)
   - Get your API key from the dashboard
   - Add to `.env`: `OPENROUTER_API_KEY=your_key_here`

2. **Groq API** (Fast & Free):
   - Sign up at [Groq](https://console.groq.com/)
   - Get your API key
   - Add to `.env`: `GROQ_TOKEN=your_key_here`

---

## Examples 

### With or Without Background Examples

| Original Video in French | ViDubb With Background in English | ViDubb Without Background in English |
| ------------------------------------------------------------ | ------------------------------------------------------------ |------------------------------------------------------ |
| <video src="https://github.com/user-attachments/assets/9b0a5f20-3be7-454c-a800-a561040592ac"> | <video src="https://github.com/user-attachments/assets/64074f56-61e3-497a-8cc2-c400190b9029"> |<video src="https://github.com/user-attachments/assets/8339550b-d60b-43b2-852f-d89d08e814d3"> |



### LipSync Example

| Original Video in English                                    | ViDubb with LipSync in French                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| <video src="https://github.com/user-attachments/assets/78be408d-255d-4ceb-a2fd-099f75134263"> | <video src="https://github.com/user-attachments/assets/8ad5945e-4d99-4a5a-967c-b2521b2cfa64"> |


> [!NOTE]
>
> Due to GitHub restrictions, we had to clip and downgrade the linked examples.
>
> To view the original videos, please visit our [YouTube channel](https://www.youtube.com/@medahmedkrichen). Don't forget to subscribe!


---

<details open>

<summary>Table of Contents </summary>

1. [Introduction](#introduction)
   - [Key Features](#key-features)
2. [TO DO List](#to-do-list)
3. [ViDubb Installation and Usage Guide](#vidubb-installation-and-usage-guide)
   - [0) Install Anaconda](#0-install-anaconda)
   - [1) Set Up the Conda Environment](#1-set-up-the-conda-environment)
   - [2) Clone the Repository](#2-clone-the-repository)
   - [3) Configure the `.env` File](#3-configure-the-env-file)
   - [4) Install Dependencies](#4-install-dependencies)
   - [5) Configure CUDA for GPU Acceleration](#5-configure-cuda-for-gpu-acceleration)
   - [6) Download Wave2Lip Models](#6-download-wave2lip-models)
   - [7) Run the Project](#7-run-the-project)
   - [8) Launch the Gradio Web App](#8-launch-the-gradio-web-app)
4. [Google Cloud TTS Setup](#google-cloud-tts-setup)
5. [Detailed Features and Technical Details](#detailed-features-and-technical-details)
   - [Speaker Diarization](#speaker-diarization)
   - [Lip-Sync (Optional)](#lip-sync-optional)
   - [Text Transcription](#text-transcription)
   - [Sentence Segmentation](#sentence-segmentation)
   - [Text Translation](#text-translation)
   - [Emotion Analysis (Optional)](#emotion-analysis-optional)
   - [Audio Synthesis](#audio-synthesis)
   - [Audio and Video Synchronization](#audio-and-video-synchronization)
   - [Audio and Video Mixing](#audio-and-video-mixing)
6. [Acknowledgment](#acknowledgment)
7. [License](#license)


</details>


## Introduction

**ViDubb** (Video dubber) is an advanced AI-powered video dubbing solution designed to deliver high-quality, efficient dubbing for multilingual content. By integrating cutting-edge voice cloning technology and dynamic lip-sync synchronization, ViDubb ensures that voiceovers are perfectly aligned with the original video's dialogue and actor movements, even when multiple speakers are involved, providing a seamless viewing experience across languages.

Leveraging state-of-the-art AI, **ViDubb** sets new standards in dubbing accuracy and naturalness, making it ideal for global content localization, film, media, and educational purposes. The tool enables content creators and businesses to quickly adapt their videos for international audiences while maintaining top-tier audio and visual quality.

### Key features include:

- **Download Direct Video from YouTube**: Allows users to download videos directly from YouTube for immediate dubbing and localization, saving time and simplifying the workflow.
- **Multi-Language Support**: Offers dubbing in a variety of languages, ensuring broad global accessibility.
- **AI Voice Cloning**: Creates realistic, high-quality voiceovers that capture the tone and emotion of the original content.
- **Google Cloud TTS Integration**: Premium voice synthesis with Google's neural voices for enhanced quality.
- **Enhanced Translation APIs**: OpenRouter and Groq integration for superior translation accuracy.
- **Dynamic Lip-Sync Technology**: Ensures perfect synchronization with video visuals, even when multiple speakers are involved, enhancing realism and interactivity.
- **Background Sound Preservation**: Retains original background sounds to maintain the authenticity of the video.
- **Efficient Dubbing Process**: Streamlines the video dubbing workflow, enabling faster and more cost-effective localization.
- **Sentence Tokenization**: Breaks down content into manageable segments for better translation and synchronization.
- **Speaker Diarization**: Identifies and separates speakers in the audio, ensuring accurate voice assignment for each speaker during dubbing.
- **Web Interface Support**: Provides an intuitive web interface for easy upload, management, and control of dubbing projects.
- **CPU and GPU Compatibility**: Works seamlessly on both CPU and GPU systems, optimizing performance based on available resources.

Our mission is to provide an efficient and high-quality AI-driven dubbing solution that empowers content creators to expand their global reach, bringing videos to audiences in multiple languages with perfect synchronization and immersive quality.


---

## TO DO LIST

- [ ] Use subs if existed
- [ ] Implement sentence summarization.
- [ ] Improve the Dynamic Lip-Sync Technology with a lot of speakers.
- [ ] Deploy ViDubb on HuggingFace space
- [ ] Deploy ViDubb on Docker hub
- [ ] ADD subtitles feature
- [x] Google Cloud TTS Integration
- [x] OpenRouter API Integration
      

---

## ViDubb Installation and Usage Guide

ViDubb is an AI-powered video dubbing project that involves voice cloning, multilingual capabilities, lip-syncing, and background sound preservation. Follow the steps below to set up and run ViDubb.

### 0) Install Anaconda
Before starting, ensure you have [Anaconda](https://docs.anaconda.com/anaconda/install/) installed on your system. Anaconda is used to manage Python environments and dependencies.

### 1) Set Up the Conda Environment
1. **Remove any existing environment** (if necessary):
    ```bash
    conda remove -n vidubbtest --all
    ```

2. **Create a new conda environment** with Python 3.10.14 and IPython:
    ```bash
    conda create -n "vidubbtest" python=3.10.14 ipython
    ```

3. **Activate the environment**:
    ```bash
    conda activate vidubbtest
    ```

### 2) Clone the Repository
1. **Clone the ViDubb repository** from GitHub:
    ```bash
    git clone https://github.com/medahmedkrichen/ViDubb.git
    ```

2. **Navigate to the ViDubb directory**:
    ```bash
    cd ViDubb
    ```

### 3) Configure the `.env` File
1. **Set up the `.env` file** with your API tokens:
    - Create a `.env` file in the `ViDubb` directory.
    - Add the following lines:
    ```bash
    HF_TOKEN="your_huggingface_token"
    Groq_TOKEN="your_groq_token"
    
    # OpenRouter API Configuration (Optional - for premium translation)
    OPENROUTER_API_KEY="your_openrouter_api_key"
    
    # Google Cloud TTS Configuration (Optional)
    GOOGLE_CLOUD_CREDENTIALS_PATH="path/to/your/google-cloud-credentials.json"
    USE_GOOGLE_TTS=false
    ```
> [!NOTE]
>
> You can obtain your `HF_TOKEN` from [Hugging Face](https://huggingface.co/settings/tokens) to use the **speaker separation**, make sure to request access to [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1).
> 
> You can obtain your `Groq_TOKEN` from [GroqCloud](https://console.groq.com/keys) to use the free API model 'llama3-70b' for translation instead of the standard model (optional).
>
> You can obtain your `OPENROUTER_API_KEY` from [OpenRouter](https://openrouter.ai/) for access to premium translation models like Claude 3.5 Sonnet and GPT-4.


> [!TIP]
>
> "llama3-70b" is effective for translating languages in the Latin language family, but it is not as effective for languages like Arabic or Mandarin. If you choose not to use it, leave the groq field empty.

### 4) Install Dependencies
1. **Install FFmpeg** (for audio/video processing):
    ```bash
    sudo apt-get install ffmpeg
    ```

2. **Install Python dependencies** from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

### 5) Configure CUDA for GPU Acceleration
1. **Install PyTorch with CUDA support** for GPU acceleration:
    ```bash
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    ```

2. **Check if CUDA is available**:
    Open a Python shell and run the following:
    ```python
    import torch
    print(torch.cuda.is_available())
    ```

### 6) Download Wave2Lip Models
1. **Download the Wav2Lip model**:
    ```bash
    wget 'https://github.com/medahmedkrichen/ViDubb/releases/download/weights2/wav2lip_gan.1.1.pth' -O 'Wav2Lip/wav2lip_gan.pth'
    ```

2. **Download the face detection model**:
    ```bash
    wget "https://github.com/medahmedkrichen/ViDubb/releases/download/weights1/s3fd-619a316812.1.1.pth" -O "Wav2Lip/face_detection/detection/sfd/s3fd.pth"
    ```

### 7) Run the Project

1. **Run the inference script** to process a video:
   
    ```bash
    python inference.py --yt_url "https://www.youtube.com/shorts/ULptP9egQ6Q" --source_language "en" --target_language "fr" --LipSync True --Bg_sound True
    ```
    
    This command will:
    - --yt_url: Download the video from YouTube you can change it to "--video_url" if you want to work with local file.
    - --LipSync True: Perform lip-sync translation
    - --source_language "en" from English
    - --target_language "fr" to French.
    - --Bg_sound True preserve the bacground sounds in wanted
    - Output a dubbed video with lip-syncing in results.
  
More options:

```bash
usage: inference.py [-h] (--yt_url YT_URL | --video_url VIDEO_URL)
                    --source_language SOURCE_LANGUAGE --target_language
                    TARGET_LANGUAGE [--whisper_model WHISPER_MODEL]
                    [--LipSync LIPSYNC] [--Bg_sound BG_SOUND]
Choose between YouTube or video URL

options:
  -h, --help            show this help message and exit
  --yt_url YT_URL       YouTube single video URL
  --video_url VIDEO_URL
                        Single video URL
  --source_language SOURCE_LANGUAGE
                        Video source language
  --target_language TARGET_LANGUAGE
                        Video target language
  --whisper_model WHISPER_MODEL
                        Chose the whisper model based on your device
                        requirements
  --LipSync LIPSYNC     Lip synchronization of the resut audio to the
                        synthesized video
  --Bg_sound BG_SOUND   Keep the background sound of the original video,
                        though it might be slightly noisy
```
<p align="center"><img src="images/inference.png" width="800" height="400" alt="Video dubbing">

> [!TIP]
>  --Bg_sound True: can lead to more noise in some videos with less background sound in origin video
> 
>  --LipSync True: will take more time and more memory


### 8) Launch the Gradio Web App
1. **Start the web application**:
    ```bash
    python app.py
    ```

2. **Access the app** by opening a browser and going to:
    ```
    http://localhost:7860/
    ```
<p align="center"><img src="images/gradio app.jpeg" width="900" height="650" alt="Video dubbing">

By following these steps, you should be able to set up and run ViDubb for video dubbing with AI-powered voice and lip synchronization.

---

## Google Cloud TTS Setup

To use Google Cloud Text-to-Speech for enhanced voice quality:

### 1) Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Text-to-Speech API

### 2) Create Service Account
1. Navigate to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Give it a name and description
4. Grant the "Text-to-Speech Client" role
5. Create and download the JSON key file

### 3) Configure ViDubb
1. Place the JSON credentials file in your project directory
2. Update your `.env` file:
   ```bash
   GOOGLE_CLOUD_CREDENTIALS_PATH="path/to/your/google-cloud-credentials.json"
   USE_GOOGLE_TTS=true
   ```

### 4) Verify Setup
Run the setup verification:
```python
from config.google_cloud_setup import setup_google_cloud_credentials, validate_google_cloud_credentials

creds_path = setup_google_cloud_credentials()
if creds_path and validate_google_cloud_credentials(creds_path):
    print("Google Cloud TTS is ready!")
else:
    print("Google Cloud TTS setup incomplete")
```

---

## Detailed Features and Technical Details


The provided code implements a robust video dubbing pipeline, leveraging various machine learning and audio/video processing techniques. Here's a detailed breakdown of the key features and their underlying technical implementations:

**- Speaker Diarization**
* **Technical Implementation:** Employs the `pyannote.audio` library, a state-of-the-art speaker diarization toolkit. It segments the audio into speaker turns, allowing for accurate identification of who is speaking at any given time.

**- Lip-Sync (Optional)**
* **Technical Implementation:**
  - **Frame Extraction:** Uses OpenCV to extract frames from the video based on the speaker diarization results.
  - **Face Detection:** Leverages the Haar Cascade classifier or a more advanced deep learning-based face detector to locate faces within each frame.
  - **Face Alignment and Normalization:** Prepares the detected faces for further processing by aligning them to a standard template.
  - **Lip-Sync Model:** Employs a pre-trained lip-sync model, such as Wav2Lip, to generate realistic lip movements based on the input audio and extracted facial features.

**- Text Transcription**
* **Technical Implementation:** Leverages the Whisper model, a robust speech-to-text model, to transcribe the audio content of the video into text. This provides a textual representation of the audio, which is crucial for subsequent text-based processing.

**- Sentence Segmentation**
* **Technical Implementation:** Utilizes the NLTK library's sentence tokenization capabilities to divide the transcribed text into meaningful sentences. This segmentation is essential for accurate translation and emotion analysis.

**- Text Translation**
* **Technical Implementation:**
  - **Enhanced Translation Service:** Uses multiple AI providers including OpenRouter (Claude 3.5 Sonnet, GPT-4, Gemini Pro) and Groq (Llama 3 models) for superior translation quality.
  - **Context-Aware Translation:** Provides sentence context to improve translation accuracy and maintain narrative flow.
  - **Automatic Fallback:** Intelligently selects the best available provider and falls back to MarianMT if API services are unavailable.

**- Emotion Analysis (Optional)**
* **Technical Implementation:** Leverages a pre-trained emotion recognition model, such as the one provided by SpeechBrain, to analyze the emotions expressed in the audio segments. The model classifies emotions into categories like anger, happiness, sadness, and neutral.

**- Audio Synthesis**
* **Technical Implementation:** 
  - **Coqui TTS:** Employs a text-to-speech (TTS) system, such as the one provided by the TTS library, to synthesize audio from the translated text. The TTS system can be further customized to match the speaker's voice and emotion.
  - **Google Cloud TTS:** Uses Google's neural text-to-speech API for premium voice quality with multiple voice options and enhanced naturalness.

**- Audio and Video Synchronization**
* **Technical Implementation:** Leverages FFmpeg to synchronize the generated audio with the original video, ensuring that the lip movements align with the spoken words.

**- Audio and Video Mixing**
* **Technical Implementation:** Employs libraries like PyDub to mix the original video with the newly generated audio, creating the final dubbed video.

By combining these techniques and leveraging the power of machine learning, the code effectively addresses the challenges of video dubbing, delivering high-quality results.

---
## Acknowledgment
- [Linly Dubbing](https://github.com/Kedreamix/Linly-Dubbing/tree/main)
- [Wav2Lip](https://github.com/zabique/Wav2Lip)
- [freeCodeCamp](https://github.com/freeCodeCamp/freeCodeCamp)
- [HuggingFace video-dubbing](https://huggingface.co/spaces/artificialguybr/video-dubbing)
- [Kaggle free Notebook](https://www.kaggle.com/)
- [Colab free Notebook](https://colab.research.google.com/)
- [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech)
- [OpenRouter](https://openrouter.ai/)
- [Groq](https://groq.com/)
- All open source models :)
  
---

## License

> [!Caution]
>
> When using this tool, please comply with relevant laws, including copyright, data protection, and privacy laws. Do not use this tool without permission from the original author and/or rights holder.

`ViDubb` follows the Apache License 2.0. When using this tool, please comply with relevant laws, including copyright, data protection, and privacy laws. Do not use this tool without permission from the original author and/or rights holder.

---

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="AI video dubbing with high-quality voice and emotion cloning for multilingual content. Sync voices with perfect lip-sync and background sound preservation.">
    <meta name="keywords" content="AI video dubbing, voice cloning, emotion cloning, multilingual dubbing, lip-sync AI, video dubbing automation, high-quality video dubbing, AI for video localization">
   <meta name="og:title" content="AI Dubbing"> 
    <meta name="og:description" content="AI video dubbing dubber Ai dubbing translation">
    <meta name="og:image" content="https://example.com/ai-video-dubbing.jpg">
    <meta name="og:type" content="website">
    <meta name="og:url" content="ai-video-dubbing">
    <meta name="description" content="ai video dubbing">
    <meta name="description" content="ai video dubbing">
    <meta name="description" content="ai video dubbing">
    <meta name="description" content="ai video dubbing">
    <meta name="description" content="ai video dubbing">
    <meta name="description" content="ai video dubbing">
    <meta name="description" content="ai dubbing">
    <meta name="description" content="ai dubbing">
    <meta name="description" content="ai dubbing">
    <meta name="description" content="video dubbing">
    <meta name="description" content="video dubbing">
    <meta name="description" content="video dubbing">
    <meta name="description" content="video dubbing">
    <meta name="description" content="video dubbing">
    

    
</head>
<body>
    <!-- Content related to AI video dubbing -->
</body>
</html>
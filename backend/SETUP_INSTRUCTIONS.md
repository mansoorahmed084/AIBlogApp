# YouTube Blog Generator - Setup Instructions

## Prerequisites

1. **Python 3.8+** installed
2. **FFmpeg** installed and available in PATH (required for audio extraction)
3. **API Keys** for:
   - OpenAI API (for blog generation and Whisper transcription)
   - Google Cloud Speech-to-Text (optional, for transcription)

## Installation Steps

### 1. Install Python Dependencies

```bash
cd C:\temp\AI\AI_blog_app\backend
pip install -r requirements.txt
```

### 2. Install FFmpeg

**Windows:**
- Download from: https://ffmpeg.org/download.html
- Extract and add `ffmpeg.exe` to your system PATH
- Or use chocolatey: `choco install ffmpeg`

**Verify installation:**
```bash
ffmpeg -version
```

### 3. Set Up API Keys

#### Option A: OpenAI API (Recommended - Handles both transcription and blog generation)

1. Get your API key from: https://platform.openai.com/api-keys
2. Set environment variable:
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # Windows CMD
   set OPENAI_API_KEY=your-api-key-here
   
   # Or add to .env file (recommended)
   ```

#### Option B: Google Cloud Speech-to-Text (Optional)

1. Create a Google Cloud project
2. Enable Speech-to-Text API
3. Create a service account and download JSON credentials
4. Set environment variable:
   ```bash
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\credentials.json"
   ```

### 4. Create .env File (Recommended)

Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=your-openai-api-key-here
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\google-credentials.json
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### 5. Update Django Settings (Optional)

If using `.env` file, install `python-dotenv`:

```bash
pip install python-dotenv
```

Then update `settings.py` to load environment variables:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 6. Run Database Migrations

```bash
python manage.py migrate
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

## Usage

1. **Sign up** or **log in** to your account
2. Go to the home page
3. Paste a YouTube video URL
4. Click "Generate Blog"
5. Wait for processing (download → transcribe → generate)
6. View your generated blog post!

## How It Works

1. **Video Download**: Uses `yt-dlp` to download audio from YouTube
2. **Transcription**: 
   - Primary: Google Cloud Speech-to-Text (if configured)
   - Fallback: OpenAI Whisper API
3. **Blog Generation**: Uses OpenAI GPT-3.5-turbo to create a structured blog post

## Troubleshooting

### "FFmpeg not found"
- Ensure FFmpeg is installed and in your PATH
- Restart terminal after adding to PATH

### "API key not found"
- Check environment variables are set correctly
- Restart Django server after setting environment variables

### "Could not download audio"
- Check internet connection
- Verify YouTube URL is valid
- Some videos may be region-restricted or age-restricted

### "Transcription failed"
- Check API credentials are valid
- Ensure you have API credits/quota available
- Try a shorter video first

## Cost Considerations

- **OpenAI API**: 
  - Whisper: ~$0.006 per minute
  - GPT-3.5-turbo: ~$0.002 per 1K tokens
- **Google Speech-to-Text**: 
  - First 60 minutes/month free
  - Then ~$0.006 per minute

## Notes

- Longer videos take more time and cost more
- Processing time depends on video length and API response times
- Generated blog posts are saved to the database automatically

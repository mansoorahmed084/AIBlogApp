# Free API Setup Guide

This guide shows you how to set up **100% FREE** alternatives for transcription and blog generation with excellent accuracy.

## 🎯 Recommended FREE Setup (Best Accuracy)

### Option 1: Completely Free (No API Keys Needed!)

**Transcription:** Local Whisper (runs on your computer)
**Blog Generation:** Groq API (free tier) or Google Gemini (free tier)

#### Setup Steps:

1. **Install Local Whisper** (for transcription):
   ```bash
   pip install openai-whisper
   ```
   - ✅ 100% FREE
   - ✅ No API key needed
   - ✅ Excellent accuracy
   - ✅ Works offline
   - ⚠️ First run downloads model (~500MB-3GB depending on model size)

2. **Get Groq API Key** (for blog generation):
   - Go to: https://console.groq.com/
   - Sign up (free)
   - Create API key
   - **Option A:** Save to file (recommended):
     - Create file: `C:\temp\AI\secret keys\groq_api_key.txt`
     - Paste your API key in the file (just the key, no quotes)
   - **Option B:** Set environment variable:
     ```powershell
     $env:GROQ_API_KEY="your-groq-api-key"
     ```
   - ✅ FREE tier: Very generous limits
   - ✅ Very fast (uses Llama models)
   - ✅ Excellent quality

3. **OR Get Google Gemini API Key** (alternative):
   - Go to: https://makersuite.google.com/app/apikey
   - Sign up (free)
   - Create API key
   - Set environment variable:
     ```powershell
     $env:GEMINI_API_KEY="your-gemini-api-key"
     ```
   - ✅ FREE tier: 60 requests/minute
   - ✅ Good quality

### Option 2: Free API Services

#### Transcription APIs (Free Tiers):

1. **AssemblyAI** (Recommended)
   - Free tier: **5 hours/month**
   - Sign up: https://www.assemblyai.com/
   - Get API key and save:
     - **Option A:** Save to file (recommended):
       - Create file: `C:\temp\AI\secret keys\assemblyAI_key.txt`
       - Paste your API key in the file (just the key, no quotes)
     - **Option B:** Set environment variable:
       ```powershell
       $env:ASSEMBLYAI_API_KEY="your-assemblyai-key"
       ```
   - ✅ High accuracy
   - ✅ Easy to use

2. **Deepgram**
   - Free tier: Available
   - Sign up: https://deepgram.com/
   - Get API key and set:
     ```powershell
     $env:DEEPGRAM_API_KEY="your-deepgram-key"
     ```

#### Blog Generation APIs (Free Tiers):

1. **Groq** (Best Free Option)
   - Free tier: Very generous
   - Fast and high quality
   - Uses Llama 3.1 70B model
   - Sign up: https://console.groq.com/

2. **Google Gemini**
   - Free tier: 60 requests/minute
   - Good quality
   - Sign up: https://makersuite.google.com/app/apikey

## 📊 Comparison Table

| Service | Type | Cost | Accuracy | Speed | Setup Difficulty |
|--------|------|------|----------|-------|------------------|
| **Local Whisper** | Transcription | FREE | ⭐⭐⭐⭐⭐ | Medium | Easy |
| **AssemblyAI** | Transcription | FREE (5hrs/mo) | ⭐⭐⭐⭐⭐ | Fast | Easy |
| **Deepgram** | Transcription | FREE tier | ⭐⭐⭐⭐ | Fast | Easy |
| **Groq** | Blog Gen | FREE | ⭐⭐⭐⭐⭐ | Very Fast | Easy |
| **Gemini** | Blog Gen | FREE | ⭐⭐⭐⭐ | Fast | Easy |
| OpenAI GPT | Blog Gen | Paid | ⭐⭐⭐⭐⭐ | Medium | Easy |
| Google Speech | Transcription | FREE (60min/mo) | ⭐⭐⭐⭐⭐ | Fast | Medium |

## 🚀 Quick Start (Recommended Free Setup)

1. **Install dependencies:**
   ```bash
   pip install openai-whisper requests google-generativeai
   ```

2. **Get Groq API key:**
   - Visit: https://console.groq.com/
   - Sign up and create API key

3. **Set Groq API Key** (choose one method):
   - **Method 1 (Recommended):** Save to file:
     - Create directory: `C:\temp\AI\secret keys\`
     - Create file: `groq_api_key.txt`
     - Paste your API key (just the key, no quotes or extra text)
   - **Method 2:** Set environment variable:
     ```powershell
     $env:GROQ_API_KEY="your-groq-api-key"
     ```

4. **That's it!** The system will automatically:
   - Use local Whisper for transcription (FREE)
   - Use Groq for blog generation (FREE)

## 💡 How It Works

The system tries APIs in this order (first available wins):

**Transcription Priority:**
1. Local Whisper (FREE, no API needed)
2. AssemblyAI (FREE tier)
3. Deepgram (FREE tier)
4. Google Speech-to-Text (FREE 60min/month)
5. OpenAI Whisper API (paid)

**Blog Generation Priority:**
1. Groq API (FREE)
2. Google Gemini (FREE)
3. OpenAI GPT (paid)

## 🎯 Best Free Combination

**Recommended:** Local Whisper + Groq API
- ✅ 100% free
- ✅ Excellent accuracy
- ✅ Very fast
- ✅ No monthly limits (except Groq rate limits)

## 📝 API Key Setup Methods

### Method 1: File-Based (Recommended)
Create files in: `C:\temp\AI\secret keys\`
- `groq_api_key.txt` - For Groq API (blog generation)
- `assemblyAI_key.txt` - For AssemblyAI API (transcription)
- Just paste your API key in each file (no quotes, no extra text)
- The system will automatically read them

### Method 2: Environment Variables
```powershell
# FREE Options (Recommended)
$env:GROQ_API_KEY="your-key"              # Blog generation (or use file method above)
$env:GEMINI_API_KEY="your-key"             # Alternative blog generation
$env:ASSEMBLYAI_API_KEY="your-key"         # Transcription (5hrs/month free)
$env:DEEPGRAM_API_KEY="your-key"           # Alternative transcription

# Paid Options (Optional)
$env:OPENAI_API_KEY="your-key"             # Blog generation + Whisper API
$env:GOOGLE_APPLICATION_CREDENTIALS="path"  # Google Speech-to-Text
```

**Note:** The system checks files first (`C:\temp\AI\secret keys\groq_api_key.txt` and `assemblyAI_key.txt`), then falls back to environment variables.

### File-Based API Keys Supported:
- ✅ Groq: `C:\temp\AI\secret keys\groq_api_key.txt`
- ✅ AssemblyAI: `C:\temp\AI\secret keys\assemblyAI_key.txt`

## ⚠️ Notes

- **Local Whisper** requires downloading a model on first use (~500MB-3GB)
- **Groq** has rate limits but very generous free tier
- **AssemblyAI** free tier: 5 hours/month
- All free APIs have rate limits, but they're usually sufficient for personal use

## 🔧 Troubleshooting

### "Whisper model not found"
- First run downloads the model automatically
- Check internet connection
- Model size options: tiny, base, small, medium, large

### "API key not found"
- Make sure environment variables are set
- Restart Django server after setting variables
- Check variable names are correct

### "Rate limit exceeded"
- Free tiers have limits
- Wait a bit and try again
- Consider using local Whisper for transcription (no limits)

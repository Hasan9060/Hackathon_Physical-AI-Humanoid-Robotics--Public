# Chapter Translation Implementation Guide

## Overview
This guide explains how to use and maintain the chapter-by-chapter Urdu translation feature in your Docusaurus-based Physical AI & Humanoid Robotics textbook.

## ✨ Features

- **Per-Chapter Translation**: Each chapter can be translated independently
- **Dropdown Interface**: Clean, professional dropdown at the start of each chapter
- **Loading Indicators**: Real-time progress tracking with chunk-based translation
- **i18n Integration**: Uses Docusaurus i18n configuration
- **Chunk-Based Processing**: Large chapters are split into manageable chunks (~4000 characters)
- **HTML Preservation**: Maintains all formatting, links, code blocks, and structure
- **RTL Support**: Proper right-to-left text rendering for Urdu
- **Caching**: Translations are cached in localStorage to avoid re-translation
- **Dark Mode**: Full support for light and dark themes

## 🏗️ Architecture

### Frontend Components

1. **ChapterTranslationDropdown** (`src/components/ChapterTranslationDropdown/index.tsx`)
   - Main translation UI component
   - Handles user interaction and translation state
   - Manages progress tracking and content display

2. **DocItem Content Wrapper** (`src/theme/DocItem/Content/index.tsx`)
   - Integrates translation dropdown into every chapter
   - Swizzled Docusaurus theme component

### Backend Components

1. **Translation Endpoints** (`backend/translation_endpoints.py`)
   - `/api/v1/translate-chunk`: Translates individual content chunks
   - `/api/v1/translate/health`: Health check endpoint
   - Uses OpenAI GPT-4 for high-quality translation

2. **Main API** (`backend/main.py`)
   - Integrates translation routes
   - Handles CORS and authentication

## 📋 Prerequisites

### Backend Requirements
```bash
# Python packages (already in requirements.txt)
- fastapi
- openai
- python-dotenv
- uvicorn
```

### Frontend Requirements
```bash
# npm packages (already in package.json)
- @docusaurus/core
- @docusaurus/preset-classic
- react
- react-dom
```

### Environment Variables
Create a `.env` file in the `backend` directory:

```env
# OpenAI API Key (required for translation)
OPENAI_API_KEY=your_openai_api_key_here

# Chat model (optional, defaults to gpt-4-turbo-preview)
CHAT_MODEL=gpt-4-turbo-preview

# Other existing variables...
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

## 🚀 Setup Instructions

### Step 1: Configure Docusaurus i18n

The `docusaurus.config.ts` is already configured with Urdu support:

```typescript
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'ur'],
  localeConfigs: {
    ur: {
      label: 'اردو',
      direction: 'rtl',
      htmlLang: 'ur-PK',
      calendar: 'gregory',
    },
  },
}
```

### Step 2: Start the Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the server
python main.py
```

The backend will run on `http://localhost:8000`

### Step 3: Start the Frontend

```bash
# From the root directory
npm start
```

The frontend will run on `http://localhost:3000`

### Step 4: Test Translation

1. Navigate to any chapter in your textbook
2. You'll see a "Translate / ترجمہ کریں" button at the top
3. Click the button to open the language dropdown
4. Select "اردو" (Urdu)
5. Watch the progress indicator as the chapter is translated
6. View the translated content in Urdu with proper RTL formatting

## 🔧 How It Works

### Translation Flow

```
User clicks "Translate" 
  ↓
Dropdown shows language options
  ↓
User selects Urdu
  ↓
Frontend extracts chapter HTML content
  ↓
Content is split into ~4000 character chunks
  ↓
Each chunk is sent to backend sequentially
  ↓
Backend uses OpenAI to translate while preserving HTML
  ↓
Frontend displays progress (chunk X of Y)
  ↓
Translated chunks are reassembled
  ↓
Original content is hidden, translated content shown
  ↓
Translation cached in localStorage
```

### Chunk Processing

The frontend splits content intelligently:
- **Chunk size**: ~4000 characters
- **Smart splitting**: Avoids breaking HTML tags or sentences
- **Sequential processing**: One chunk at a time to show progress
- **Tag preservation**: HTML structure maintained throughout

### Backend Translation

The backend (`translation_endpoints.py`):
1. Receives HTML chunk
2. Cleans unnecessary elements (scripts, styles)
3. Protects HTML tags with placeholders
4. Sends text to OpenAI for translation
5. Restores HTML tags in translated text
6. Returns translated HTML chunk

## 🎨 Customization

### Adding More Languages

Edit `src/components/ChapterTranslationDropdown/index.tsx`:

```typescript
const languages = [
  { code: 'en', name: 'English', flag: '🇺🇸', direction: 'ltr' },
  { code: 'ur', name: 'اردو', flag: '🇵🇰', direction: 'rtl' },
  // Add more languages:
  { code: 'ar', name: 'العربية', flag: '🇸🇦', direction: 'rtl' },
  { code: 'es', name: 'Español', flag: '🇪🇸', direction: 'ltr' },
];
```

Also update `docusaurus.config.ts`:

```typescript
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'ur', 'ar', 'es'],
  localeConfigs: {
    ur: { /* ... */ },
    ar: { /* ... */ },
    es: { /* ... */ },
  },
}
```

### Adjusting Chunk Size

In `src/components/ChapterTranslationDropdown/index.tsx`, line 115:

```typescript
const chunkSize = 4000; // Adjust this value
```

Smaller chunks = more API calls but better progress tracking
Larger chunks = fewer API calls but slower progress updates

### Styling Changes

Edit `src/components/ChapterTranslationDropdown/styles.module.css`:

- **Button colors**: `.triggerButton` section
- **Dropdown appearance**: `.dropdownMenu` section
- **Progress modal**: `.progressModal` and `.progressContent`
- **Dark mode**: `[data-theme='dark']` selectors
- **RTL styling**: `.translationDropdown[dir='rtl']` selectors

### Translation Model

In `backend/translation_endpoints.py`, line 117:

```python
model=os.getenv("CHAT_MODEL", "gpt-4-turbo-preview"),
```

Options:
- `gpt-4-turbo-preview`: Best quality, slower, more expensive
- `gpt-3.5-turbo`: Faster, cheaper, good quality
- `gpt-4o`: Balanced option

## 🐛 Troubleshooting

### Translation Button Not Showing

**Check:**
1. Is the component imported in `src/theme/DocItem/Content/index.tsx`?
2. Are you on a chapter page (not homepage)?
3. Check browser console for errors

**Fix:**
```bash
npm start
# Clear browser cache and reload
```

### Backend Not Responding

**Check:**
1. Is the backend running? Visit `http://localhost:8000`
2. Is the OpenAI API key set in `.env`?
3. Check backend terminal for errors

**Fix:**
```bash
cd backend
python main.py
# Check for error messages
```

### Translation Fails

**Common causes:**
1. **No OpenAI API key**: Set `OPENAI_API_KEY` in `.env`
2. **API rate limit**: Wait a moment and try again
3. **Network issues**: Check internet connection
4. **Invalid API key**: Verify your OpenAI key is active

**Check backend logs:**
```bash
# Backend terminal will show:
Translation error: [error message]
```

### Progress Stuck at 0%

**Causes:**
1. Backend not receiving requests (CORS issue)
2. Content extraction failed
3. API timeout

**Fix:**
1. Check browser Network tab for failed requests
2. Verify CORS is enabled in `backend/main.py`
3. Try translating a smaller chapter first

### Urdu Text Not Displaying Correctly

**Causes:**
1. Missing Urdu fonts
2. RTL direction not applied
3. Browser doesn't support Unicode

**Fix:**
1. The component uses Google Fonts (Noto Nastaliq Urdu)
2. Check if `direction: rtl` is applied in browser inspector
3. Try a modern browser (Chrome, Firefox, Edge)

### Translation Not Cached

**Causes:**
1. localStorage disabled
2. Incognito/private mode
3. Browser storage full

**Fix:**
1. Enable localStorage in browser settings
2. Use normal browsing mode
3. Clear some browser storage

## 📊 Performance Considerations

### API Costs

- **Model**: GPT-4 Turbo
- **Average chapter**: 10,000-20,000 characters
- **Chunks**: 3-5 chunks per chapter
- **Cost**: ~$0.10-0.30 per chapter translation

**Optimization tips:**
1. Use caching (already implemented)
2. Consider GPT-3.5-turbo for lower costs
3. Batch translate during off-peak hours

### Translation Speed

- **Small chapter** (5,000 chars): ~10-15 seconds
- **Medium chapter** (15,000 chars): ~30-45 seconds
- **Large chapter** (30,000 chars): ~60-90 seconds

**Speed improvements:**
1. Parallel chunk processing (advanced)
2. Use faster model (GPT-3.5-turbo)
3. Increase chunk size (reduces API calls)

### Caching Strategy

Current implementation:
- **Storage**: Browser localStorage
- **Key**: `translation_${pathname}`
- **Persistence**: Until user clears cache or clicks "Show Original"

Production improvements:
- Use IndexedDB for larger storage
- Implement server-side caching (Redis)
- Add cache expiration (e.g., 30 days)

## 🔒 Security Considerations

### API Key Protection

**Current setup:**
- API key stored in backend `.env` file
- Never exposed to frontend
- Backend acts as proxy

**Production checklist:**
- [ ] Use environment variables on hosting platform
- [ ] Never commit `.env` to git (already in `.gitignore`)
- [ ] Rotate API keys regularly
- [ ] Monitor API usage

### Rate Limiting

**Recommended:**
```python
# In backend/translation_endpoints.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@translation_router.post("/translate-chunk")
@limiter.limit("10/minute")  # 10 requests per minute
async def translate_chunk(request: TranslationRequest):
    # ...
```

### Authentication

**Current:** No authentication required for translation

**Production recommendation:**
```python
# Require authentication for translation
@translation_router.post("/translate-chunk")
async def translate_chunk(
    request: TranslationRequest,
    current_user: User = Depends(get_current_user)
):
    # ...
```

## 🚀 Production Deployment

### Environment Setup

**Backend (.env):**
```env
OPENAI_API_KEY=your_production_key
CHAT_MODEL=gpt-4-turbo-preview
API_URL=https://your-backend-domain.com
```

**Frontend (docusaurus.config.ts):**
```typescript
customFields: {
  apiUrl: process.env.API_URL || 'https://your-backend-domain.com',
}
```

### Deployment Checklist

- [ ] Set production API URL in frontend
- [ ] Configure CORS for production domain
- [ ] Set up SSL/HTTPS for backend
- [ ] Implement rate limiting
- [ ] Add authentication (optional)
- [ ] Monitor API usage and costs
- [ ] Set up error logging (Sentry, etc.)
- [ ] Test translation on production

### Hosting Options

**Backend:**
- Railway (current setup)
- Heroku
- AWS Lambda
- Google Cloud Run
- DigitalOcean

**Frontend:**
- Netlify (current setup)
- Vercel
- GitHub Pages
- AWS S3 + CloudFront

## 📝 Maintenance

### Regular Tasks

1. **Monitor API costs** (weekly)
   - Check OpenAI dashboard
   - Adjust chunk size if needed

2. **Check error logs** (daily)
   - Backend translation errors
   - Frontend console errors

3. **Update dependencies** (monthly)
   ```bash
   npm update
   pip install --upgrade -r requirements.txt
   ```

4. **Test translation quality** (after updates)
   - Translate a sample chapter
   - Verify HTML preservation
   - Check RTL rendering

### Updating Translation Logic

**To modify translation prompt:**

Edit `backend/translation_endpoints.py`, line 102:

```python
system_prompt = f"""You are a professional translator...
[Modify instructions here]
"""
```

**To change HTML handling:**

Edit functions in `backend/translation_endpoints.py`:
- `clean_html_content()`: Modify HTML cleaning
- `protect_html_tags()`: Change tag protection
- `restore_html_tags()`: Adjust tag restoration

## 🎓 Best Practices

### For Users

1. **First time**: Translate a small chapter to test
2. **Wait for completion**: Don't navigate away during translation
3. **Clear cache**: If translation seems outdated
4. **Report issues**: Note which chapter had problems

### For Developers

1. **Test locally**: Always test translation before deploying
2. **Monitor costs**: Keep track of OpenAI API usage
3. **Version control**: Commit working changes
4. **Documentation**: Update this guide when making changes
5. **Error handling**: Add try-catch blocks for new features

## 📚 Additional Resources

- [Docusaurus i18n Documentation](https://docusaurus.io/docs/i18n/introduction)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Hooks Guide](https://react.dev/reference/react)

## 🆘 Support

If you encounter issues:

1. **Check this guide** for troubleshooting steps
2. **Check browser console** for frontend errors
3. **Check backend logs** for API errors
4. **Test with a simple chapter** to isolate the issue
5. **Verify environment variables** are set correctly

## 📄 File Reference

### Key Files

```
humanoid-robotics-textbook/
├── backend/
│   ├── main.py                          # Main API with translation routes
│   ├── translation_endpoints.py         # Translation logic
│   └── .env                             # Environment variables
├── src/
│   ├── components/
│   │   └── ChapterTranslationDropdown/
│   │       ├── index.tsx                # Main component
│   │       └── styles.module.css        # Styling
│   └── theme/
│       └── DocItem/
│           └── Content/
│               └── index.tsx            # Integration point
├── docusaurus.config.ts                 # i18n configuration
└── package.json                         # Frontend dependencies
```

## ✅ Quick Start Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] OpenAI API key set in backend/.env
- [ ] Navigate to any chapter
- [ ] Click "Translate / ترجمہ کریں" button
- [ ] Select "اردو" from dropdown
- [ ] Wait for translation to complete
- [ ] Verify Urdu text displays correctly with RTL
- [ ] Test "Show Original" button
- [ ] Check that translation is cached (reload page)

---

**Last Updated**: December 9, 2024
**Version**: 1.0.0
**Maintainer**: Your Name

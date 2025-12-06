# GitHub Setup Instructions

## Repository Information
- **Repository URL**: https://github.com/Hasan9060/Hackathon_Physical-AI-Humanoid-Robotics--Public.git
- **Current Branch**: 001-robotics-lab-guide
- **Status**: Remote configured, ready to push

## Pushing to GitHub

### Option 1: Using Personal Access Token (Recommended)

1. **Create a Personal Access Token**:
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token"
   - Give it a name (e.g., "Physical AI Robotics")
   - Select scopes: `repo` (Full control of private repositories)
   - Click "Generate token"
   - Copy the token (you won't see it again)

2. **Push with Token**:
   ```bash
   # Method 1: Using Git credential helper
   git push -u origin 001-robotics-lab-guide

   # When prompted for username: enter your GitHub username
   # When prompted for password: paste your personal access token
   ```

### Option 2: Using SSH Key

1. **Generate SSH Key** (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. **Add SSH Key to GitHub**:
   ```bash
   # Copy the public key
   cat ~/.ssh/id_ed25519.pub
   ```
   - Go to GitHub → Settings → SSH and GPG keys
   - Click "New SSH key"
   - Paste the public key
   - Save

3. **Update Remote URL to SSH**:
   ```bash
   git remote set-url origin git@github.com:Hasan9060/Hackathon_Physical-AI-Humanoid-Robotics--Public.git
   git push -u origin 001-robotics-lab-guide
   ```

### Option 3: Using GitHub CLI (if installed)

```bash
# Install GitHub CLI first if not installed
# Then authenticate
gh auth login

# Push to repository
git push -u origin 001-robotics-lab-guide
```

## What Will Be Pushed

Your repository contains:

### Frontend (Docusaurus Website)
- Complete Physical AI & Humanoid Robotics textbook
- Authentication system with BetterAuth
- Interactive chatbot widget
- Responsive design with custom components

### Backend (FastAPI)
- RAG-powered chatbot with Qdrant + OpenAI + Gemini
- User authentication system
- PHR (Prompt History Records) management
- Specs management system
- Content serving endpoints

### Documentation
- Complete specifications
- Prompt history records
- API documentation
- Development guides

## After Pushing

1. **Visit your repository**: https://github.com/Hasan9060/Hackathon_Physical-AI-Humanoid-Robotics--Public

2. **Check the files**:
   - All website content in `/docs`
   - Backend API in `/backend`
   - Specifications in `/specs`
   - PHRs in `/history/prompts`

3. **Next Steps**:
   - Set up GitHub Pages for frontend deployment
   - Configure backend deployment (Vercel, Heroku, or similar)
   - Add a README.md to the repository root

## Repository Structure After Push

```
Hackathon_Physical-AI-Humanoid-Robotics--Public/
├── .claude/                  # Claude Code configuration
├── .docusaurus/             # Docusaurus cache
├── backend/                  # FastAPI backend
│   ├── services/
│   │   ├── phr_service.py   # PHR management
│   │   ├── auth_service.py  # Authentication
│   │   └── rag_service.py   # RAG chatbot
│   ├── specs/               # Project specifications
│   ├── history/prompts/     # Prompt History Records
│   ├── docs/               # Copied documentation
│   └── README.md           # API documentation
├── docs/                    # Docusaurus content
│   ├── 00-intro/
│   ├── 01-ros2/
│   ├── 02-simulation/
│   ├── 03-aicontrol/
│   └── 99-hardware/
├── specs/                   # Project specifications
├── src/                     # React components
│   ├── components/
│   ├── css/
│   └── pages/
├── static/                  # Static assets
├── history/prompts/         # PHRs
├── docusaurus.config.ts     # Docusaurus config
├── sidebars.ts             # Navigation structure
└── package.json            # Dependencies
```

## Important Notes

1. **Ensure your repository is public** as the name suggests
2. **Do NOT commit sensitive data**:
   - API keys
   - Database passwords
   - Personal information
3. **The .env file should be in .gitignore** (it already is)

## Need Help?

If you encounter any issues:
1. Check your GitHub credentials
2. Ensure you have push access to the repository
3. Verify the repository URL is correct

Good luck with your Physical AI & Humanoid Robotics project! 🤖
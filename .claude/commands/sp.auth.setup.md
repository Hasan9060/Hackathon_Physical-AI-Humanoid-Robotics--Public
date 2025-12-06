---
description: Set up BetterAuth authentication in Docusaurus project with complete frontend integration
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

This command sets up complete BetterAuth authentication integration for Docusaurus projects, including:

1. **Backend Server Setup**:
   - Create separate backend directory with BetterAuth configuration
   - Configure email/password authentication provider
   - Set up SQLite database with proper schema
   - Configure CORS for cross-origin requests

2. **Frontend Integration**:
   - Install BetterAuth client packages (@better-auth/react)
   - Create AuthProvider context for authentication state management
   - Build authentication components (login/signup forms, modals)
   - Integrate with Docusaurus theme system

3. **UI Components**:
   - AuthNavButton component for navbar integration
   - AuthModal with login/signup forms
   - User dropdown with avatar and sign out functionality
   - Responsive design with mobile support

4. **Styling & Theme**:
   - Comprehensive CSS styling compatible with Docusaurus
   - Dark mode support and accessibility features
   - Mobile responsive design
   - Loading states and error handling

5. **Navigation Integration**:
   - Custom Docusaurus Navbar wrapper
   - Header integration with Sign In/Sign Up buttons
   - User state management in navigation

## Execution Steps

1. **Check Current Project Structure**:
   - Verify this is a Docusaurus project
   - Check for existing authentication components
   - Identify current package.json dependencies

2. **Create Backend Structure**:
   - Create `/backend/` directory with package.json
   - Set up BetterAuth server configuration in `/backend/src/auth.ts`
   - Configure email/password provider with SQLite database
   - Set up CORS for frontend-backend communication

3. **Install Dependencies**:
   - Add better-auth and @better-auth/react to package.json
   - Update backend package.json with required dependencies

4. **Create Frontend Components**:
   - `/src/components/AuthProvider/index.tsx` - Main AuthProvider context
   - `/src/components/AuthProvider/AuthNavButton.tsx` - Navbar integration
   - `/src/components/AuthProvider/AuthModal.tsx` - Login/signup modal
   - `/src/components/AuthProvider/styles.css` - Complete styling

5. **Docusaurus Theme Integration**:
   - Create `/src/theme/Navbar/index.tsx` to wrap original Navbar
   - Add AuthNavButton to site navigation
   - Ensure compatibility with existing Docusaurus setup

6. **Configuration & Setup**:
   - Update root package.json with authentication dependencies
   - Configure environment variables if needed
   - Set up proper session management

## Components Created

### Backend Files
- `backend/package.json` - Backend server configuration
- `backend/src/auth.ts` - BetterAuth server setup with email/password provider

### Frontend Files
- `src/components/AuthProvider/index.tsx` - React AuthProvider context
- `src/components/AuthProvider/AuthNavButton.tsx` - Navbar authentication button
- `src/components/AuthProvider/AuthModal.tsx` - Authentication modal
- `src/components/AuthProvider/styles.css` - Complete styling system
- `src/theme/Navbar/index.tsx` - Docusaurus navbar wrapper

## Features Implemented

- **Email/Password Authentication**: Complete signup and login flow
- **Session Management**: Secure session handling with 7-day expiration
- **User Interface**: Responsive, accessible authentication components
- **Navigation Integration**: Seamless header integration with user state
- **Mobile Support**: Responsive design for all screen sizes
- **Dark Mode**: Full theme compatibility with Docusaurus
- **Error Handling**: Comprehensive error states and loading indicators

## Next Steps

After setup is complete:

1. Start backend server: `cd backend && npm run dev`
2. Start Docusaurus: `npm run start`
3. Test authentication flow
4. Configure additional providers if needed

## Quality Assurance

- All components include proper TypeScript typing
- CSS uses Docusaurus-compatible variable overrides
- Responsive design tested across breakpoints
- Accessibility features implemented (ARIA labels, keyboard navigation)
- Error handling for network failures and authentication errors

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.
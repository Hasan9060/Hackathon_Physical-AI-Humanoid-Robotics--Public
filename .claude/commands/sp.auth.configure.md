---
description: Configure and customize existing BetterAuth authentication setup
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

This command configures and customizes existing BetterAuth authentication setup in Docusaurus projects.

## Configuration Options

1. **Authentication Provider Configuration**:
   - Add OAuth providers (Google, GitHub, Discord, etc.)
   - Configure email verification settings
   - Set up password policies and requirements
   - Configure session management settings

2. **UI Component Customization**:
   - Customize authentication form styling
   - Add custom form fields
   - Configure modal behavior and triggers
   - Set up custom redirect URLs

3. **Security Settings**:
   - Configure CORS settings
   - Set up rate limiting
   - Configure session expiration
   - Enable two-factor authentication

4. **Integration Settings**:
   - Configure database connections
   - Set up email service providers
   - Configure webhook endpoints
   - Set up analytics tracking

## Execution Steps

1. **Analyze Current Setup**:
   - Check existing BetterAuth configuration in `/backend/src/auth.ts`
   - Review current authentication components
   - Identify configuration needs from user input

2. **Backend Configuration Updates**:
   - Update BetterAuth server configuration
   - Add new authentication providers if requested
   - Configure security settings and session management
   - Update CORS and environment settings

3. **Frontend Component Updates**:
   - Update AuthProvider with new configuration
   - Customize authentication forms and modals
   - Add new authentication methods if needed
   - Update styling and behavior

4. **Environment and Settings**:
   - Update environment variables
   - Configure database settings
   - Set up email service integration
   - Configure production settings

## Configuration Files Modified

- `backend/src/auth.ts` - BetterAuth server configuration
- `src/components/AuthProvider/index.tsx` - React AuthProvider
- `src/components/AuthProvider/AuthNavButton.tsx` - Navigation integration
- `src/components/AuthProvider/styles.css` - Custom styling
- Environment files (`.env`, `.env.local`)

## Examples

```bash
# Add Google OAuth provider
/sp.auth.configure add google-oauth

# Configure email verification
/sp.auth.configure configure email-verification

# Set up custom styling
/sp.auth.configure customize ui-styling primary-color:#3b82f6

# Configure session timeout
/sp.auth.configure configure session-timeout 7d
```

## Validation

After configuration changes:
1. Verify backend server starts successfully
2. Test authentication flow with new settings
3. Check UI updates render correctly
4. Validate security configurations
5. Test cross-browser compatibility

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
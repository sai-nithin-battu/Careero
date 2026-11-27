# Careero

An AI-powered career guidance and educational exploration platform built for students across Class 9–12 and B.Tech to navigate academic pathways, syllabi, degrees, colleges, and creative careers independently.

**Live Demo:** [careero-phi.vercel.app](https://careero-phi.vercel.app)

---

## Key Features

- **Pathways & Syllabi Explorer:** Structured breakdowns across CBSE, IPE, NCERT, and international boards for Class 9–12 streams (PCM, PCB, Commerce, Humanities) alongside B.Tech and Diploma tracks.
- **Degrees & Colleges Directory:** Side-by-side comparison of undergraduate degrees, entrance requirements, and engineering institutions.
- **Creative & Emerging Careers:** Dedicated guides covering gaming, VFX, animation, UI/UX, and design pathways.
- **Bramhi AI Mentor:** Conversational career mentor powered by Google Gemini with bounded multi-turn context, file/image attachment support, and a relatable, reality-check coaching persona.
- **Personal Story Matcher & Voice Narration:** Matches student challenges (academic pressure, stream confusion, creative passion) with tailored motivational stories and Microsoft Edge-TTS audio narration (`en-IN-PrabhatNeural` / `en-IN-NeerjaNeural`).
- **Zero-Friction Recruiter & Guest Access:** Immediate workspace access with pre-loaded sample student profiles for zero-cost previews, plus a **Recruiter / School Code** unlock modal for unlimited live AI testing.

---

## Architecture & Security Controls

- **Backend:** Python, FastAPI, Google Gemini API, Microsoft Edge-TTS
- **Frontend:** Vanilla JavaScript, HTML5, CSS3 (`#F28C00` amber and crisp white design system)
- **Abuse & Cost Safeguards:**
  - HMAC-signed session cookies (`COOKIE_SECRET`) with strict startup validation
  - Dual-layer rate limiting (per-session guest quotas + global daily free-tier cap) with `SCHOOL_ACCESS_CODE` bypass
  - Global brute-force cooldown on access code attempts
  - Ephemeral session-only conversation history (zero server-side persistence of raw student prompts or uploaded attachments)
  - Serverless-compatible `/tmp` SQLite quota storage for Vercel deployments

---

## Environment Variables

Configure the following variables in `.env` locally or in your Vercel project settings:

```env
GEMINI_API_KEY=your_google_gemini_api_key
SCHOOL_ACCESS_CODE=your_recruiter_or_school_unlock_code
COOKIE_SECRET=a_random_secret_string_at_least_32_characters_long

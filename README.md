# CricketArena: AI-Powered Fantasy & Prediction Platform

CricketArena is a premium, cinematic web application for cricket fans, featuring live predictions, fantasy team building, and an AI-powered coach.

## 🚀 Quick Start

### Prerequisites
- Node.js v18+
- Angular CLI v18+
- Firebase CLI
- Google Cloud SDK (for Cloud Run)

### Installation
1. Clone the repository and navigate to the project root.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Initialize Tailwind CSS:
   ```bash
   # Already configured in src/styles.css using Tailwind v4
   ```
4. Start the development server:
   ```bash
   npm run start
   ```

### Backend Setup
1. **Firebase Functions**:
   ```bash
   cd functions
   npm install
   npm run build
   ```
2. **Cloud Run Proxy**:
   ```bash
   cd cloud-run
   npm install
   # Set GEMINI_API_KEY in environment
   ```

## 🏗 Architecture (6 Google Layers)
- **UX/UI**: Angular v18 with Tailwind v4 & GSAP.
- **Storage**: Cloud Firestore for real-time state.
- **Logic**: Firebase Functions (Server-side XP validation).
- **AI**: Gemini 1.5 Flash via Cloud Run Secure Proxy.
- **Messaging**: Cloud Scheduler + Pub/Sub (Midnight streak resets).
- **Analytics**: BigQuery export via Firebase Analytics.

## 🛠 Project Structure
- `/src/app/components`: Feature-specific UI components (Dashboard, Predict, etc.)
- `/functions`: Firebase Cloud Functions for backend logic.
- `/cloud-run`: TypeScript proxy for Gemini API security.
- `src/styles.css`: Tailwind v4 theme configuration.

## 📈 Future Roadmap

### Horizon 1: Enhanced Social (3 Months)
- Private leagues with custom rules.
- Real-time chat in live-match hero bands.
- Shareable "Prediction Slips" for social media.

### Horizon 2: Advanced AI (6 Months)
- Voice-activated AI Coach commands.
- Visual AI analysis of player form (OCR from match screenshots).
- Predictive "What If" simulator for fantasy points.

### Horizon 3: Platform Expansion (12 Months)
- native iOS/Android apps via Capacitor.
- Integration with live sports betting APIs (where permitted).
- NFT-based collectible badges and player cards.

## 🔑 Environment Variables
| Variable | Purpose | Location |
|----------|---------|----------|
| `FIREBASE_CONFIG` | Frontend Firebase SDK init | `environment.ts` |
| `GEMINI_API_KEY` | AI authentication | Cloud Run Secret |
| `ADMIN_SECRET` | Manual XP override key | Functions Config |

---
**CricketArena** © 2026 • Designed with Passion for the Game.

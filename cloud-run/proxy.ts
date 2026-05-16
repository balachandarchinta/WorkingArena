import express, { Request, Response } from 'express';
import { GoogleGenerativeAI } from "@google/generative-ai";
import * as dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(express.json());

const genAI = new GoogleGenerativeAI(process.env['GEMINI_API_KEY'] || '');
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

app.post('/api/coach', async (req: Request, res: Response) => {
  const { type, context } = req.body;
  
  if (!type || !context) {
    return res.status(400).json({ error: 'Missing type or context' });
  }

  const systemPrompt = `
    You are the "CricketArena AI Coach", a premium digital strategist.
    Task: Generate ${type} for the user.
    Match Context: ${JSON.stringify(context.match)}
    User Stats: Level ${context.user.level}, XP ${context.user.xp}, Streak ${context.user.streak}
    
    Response requirements:
    - Tone: Premium, professional, encouraging.
    - Format: JSON with "text" and optional "xp_value" fields.
    - If TRIVIA: Include 3 options.
    - If CHALLENGE: Define a goal like "Predict 3 boundaries in next 2 overs".
  `;
  
  try {
    const result = await model.generateContent(systemPrompt);
    const response = await result.response;
    const text = response.text();
    
    res.json({ success: true, response: text });
  } catch (error) {
    console.error('Gemini Proxy Error:', error);
    res.status(500).json({ success: false, error: 'AI engine unavailable' });
  }
});

const PORT = process.env['PORT'] || 8080;
app.listen(PORT, () => {
  console.log(`Arena AI Proxy running on port ${PORT}`);
});

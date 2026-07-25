
DEPLOYMENT STEPS - MRBELE V3

1. Get Groq Key (FREE Meta Llama): groq.com -> API Keys -> Create -> gsk_...
2. Render.com: New Web Service -> Upload server.py + requirements.txt
   Build: pip install -r requirements.txt
   Start: gunicorn server:app
   Env: GROQ_API_KEY=gsk_...
3. Test: https://your-url.onrender.com/ -> ONLINE
4. Test AutoDM ON/OFF: 
   curl -X POST https://your-url.onrender.com/settings -H "Content-Type: application/json" -d '{"auto_dm_master": false}'
5. Test Copyright:
   curl -X POST https://your-url.onrender.com/copyright/check -H "Content-Type: application/json" -d '{"text":"MVS Ventures helps startups grow"}'
6. Connect IG: developers.facebook.com -> Webhook https://your-url.onrender.com/webhook token mrbele_verify_123

ANDROID: Use same foreground service, but add buttons that call /settings API.

# MRBELE V4 - FINAL PRODUCTION - FB SDK + AutoDM ON - Created 25 July 2026
from flask import Flask, request, jsonify
import os
import requests
from difflib import SequenceMatcher

app = Flask(__name__)

# SETTINGS
SETTINGS = {
    "auto_dm_master": True,
    "auto_dm_mrbele1": True,
    "auto_dm_mvsventures": True,
    "copyright_protection": True
}

COPYRIGHT_DB = []
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")

def check_copyright(text):
    score = 100
    matches = []
    for item in COPYRIGHT_DB:
        sim = SequenceMatcher(None, text.lower(), item["caption"].lower()).ratio()
        if sim > 0.6:
            matches.append({"similarity": round(sim*100,1), "text": item["caption"]})
            score -= sim*30
    score = max(0, int(score))
    risk = "LOW" if score>=80 else "MEDIUM" if score>=50 else "HIGH"
    return {"originality_score": score, "risk_level": risk, "matches": matches}

def ask_llama(user_message, username):
    if not GROQ_API_KEY:
        return f"Hey {username}! Team MRBELE will reply soon!"
    try:
        prompt = f"You are MRBELE agent for @mrbele1 & @mvsventures. User @{username}: {user_message}. Reply short, Gen-Z Punjab vibe under 25 words."
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":prompt}],"max_tokens":120},
            timeout=15
        )
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error: {e}")
        return f"Hey {username}! Thanks for DM. We will ping you!"

# HOME WITH FB SDK - THIS FIXES META REVIEW
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>MRBELE AUTO WORKFLOW</title>
    <meta property="fb:app_id" content="1361583235948040" />
    <script>
      window.fbAsyncInit = function() {
        FB.init({
          appId : '1361583235948040',
          cookie : true,
          xfbml : true,
          version : 'v19.0'
        });
        FB.AppEvents.logPageView();
      };
      (function(d, s, id){
         var js, fjs = d.getElementsByTagName(s)[0];
         if (d.getElementById(id)) {return;}
         js = d.createElement(s); js.id = id;
         js.src = "https://connect.facebook.net/en_US/sdk.js";
         fjs.parentNode.insertBefore(js, fjs);
       }(document, 'script', 'facebook-jssdk'));
    </script>
</head>
<body style="font-family:sans-serif; text-align:center; margin-top:60px; background:#f9f9f9;">
    <h1>MRBELE V3 ONLINE 24/7</h1>
    <p>Instagram Bot for @mvsventures & @mrbele1 is LIVE ✅</p>
    <p>Facebook SDK Loaded ✅</p>
    <p><a href="/privacy">Privacy Policy</a> | <a href="/terms">Terms</a> | <a href="/data-deletion">Data Deletion</a></p>
    <p style="font-size:12px; color:gray;">App ID: 1361583235948040 | mvsventures: 2243884129743778</p>
</body>
</html>
    """

@app.route("/settings", methods=["GET","POST"])
def settings_route():
    global SETTINGS
    if request.method == "POST":
        SETTINGS.update(request.json)
        return jsonify({"success": True, "settings": SETTINGS})
    return jsonify(SETTINGS)

@app.route("/copyright/check", methods=["POST"])
def copyright_route():
    text = request.json.get("text","")
    return jsonify(check_copyright(text))

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == "mrbele_verify_123":
        return request.args.get("hub.challenge")
    return "Invalid token", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        for entry in data.get("entry", []):
            for msg in entry.get("messaging", []):
                if "message" in msg:
                    sender = msg["sender"]["id"]
                    text = msg["message"].get("text","")
                    print(f"DM from {sender}: {text}")
                    if not SETTINGS["auto_dm_master"]:
                        print("AutoDM OFF - Logged only")
                        continue
                    reply = ask_llama(text, sender)
                    # BOT SEND - NOW ACTIVE
                    requests.post(
                        f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}",
                        json={"recipient":{"id":sender},"message":{"text":reply}},
                        timeout=10
                    )
                    print(f"Sent reply: {reply}")
    except Exception as e:
        print(f"Webhook error: {e}")
    return jsonify({"status":"ok"}), 200

@app.route("/chat", methods=["POST"])
def chat_route():
    msg = request.json.get("message","")
    username = request.json.get("username","user")
    copyright_res = check_copyright(msg)
    if not SETTINGS["auto_dm_master"]:
        return jsonify({"reply":None,"status":"OFF","copyright":copyright_res})
    reply = ask_llama(msg, username)
    return jsonify({"reply":reply,"copyright":copyright_res})

@app.route('/privacy')
def privacy():
    return "Privacy Policy: This app @mvsventures bot only reads Instagram DMs to auto-reply about services. No data stored. Contact: manveer998829@gmail.com"

@app.route('/terms')
def terms():
    return "Terms: This bot is for business auto-reply only. Contact: manveer998829@gmail.com"

@app.route('/data-deletion')
def deletion():
    return "To delete your data, DM us 'DELETE MY DATA' or email manveer998829@gmail.com - We delete within 24h"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


# MRBELE AGENT V3 FINAL - AutoDM ON/OFF + Copyright + Meta Llama
from flask import Flask, request, jsonify
import os, json, requests
from datetime import datetime
from difflib import SequenceMatcher

app = Flask(__name__)

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
        return f"Hey {username}! Got your DM: {user_message}. Team MRBELE will reply soon!"
    try:
        prompt = f"You are MRBELE agent for @mrbele1 & @mvsventures. User @{username}: {user_message}. Reply short, friendly, Gen-Z Punjab vibe under 25 words."
        res = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":prompt}],"max_tokens":120}, timeout=15)
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(e)
        return f"Hey {username}! Thanks for DM. We will ping you!"

@app.route("/")
def home():
    return jsonify({"status":"MRBELE V3 ONLINE 24/7","model":"Llama-3.3-70B","settings":SETTINGS,"time":datetime.now().isoformat()})

@app.route("/settings", methods=["GET","POST"])
def settings_route():
    global SETTINGS
    if request.method=="POST":
        SETTINGS.update(request.json)
        return jsonify({"success":True,"settings":SETTINGS})
    return jsonify(SETTINGS)

@app.route("/copyright/check", methods=["POST"])
def copyright_route():
    text = request.json.get("text","")
    return jsonify(check_copyright(text))

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token")=="mrbele_verify_123":
        return request.args.get("hub.challenge")
    return "Invalid",403

@app.route("/webhook", methods=["POST"])
def webhook():
    data=request.json
    try:
        for entry in data.get("entry",[]):
            for msg in entry.get("messaging",[]):
                if "message" in msg:
                    sender=msg["sender"]["id"]
                    text=msg["message"].get("text","")
                    if not SETTINGS["auto_dm_master"]:
                        print(f"AutoDM OFF - Logged DM from {sender}: {text}")
                        continue
                    reply=ask_llama(text, sender)
                    # requests.post(f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}", json={"recipient":{"id":sender},"message":{"text":reply}})
                    print(f"Auto Reply: {reply}")
    except Exception as e:
        print(e)
    return jsonify({"status":"ok"})

@app.route("/chat", methods=["POST"])
def chat_route():
    msg=request.json.get("message","")
    username=request.json.get("username","user")
    copyright_res=check_copyright(msg)
    if not SETTINGS["auto_dm_master"]:
        return jsonify({"reply":None,"status":"AutoDM OFF - Logged only","copyright":copyright_res})
    reply=ask_llama(msg, username)
    return jsonify({"reply":reply,"copyright":copyright_res})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)

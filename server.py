# MRBELE V4 - META APPROVED VERSION with FB.getLoginStatus
from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")

def ask_llama(m,u):
    try:
        r=requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization":f"Bearer {GROQ_API_KEY}"},
        json={"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":f"User {u}: {m}. Reply Gen-Z Punjab short"}]},
        timeout=10)
        return r.json()["choices"][0]["message"]["content"]
    except: return f"Hey {u}! Team MRBELE will reply soon!"

@app.route("/")
def home():
    # THIS IS META REQUIRED CODE - with FB.getLoginStatus
    return """
<!DOCTYPE html>
<html>
<head>
<title>MRBELE AUTO WORKFLOW</title>
<meta property="fb:app_id" content="1361583235948040" />
</head>
<body>
<script>
  function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    if (response.status === 'connected') {
      testAPI();
    } else {
      document.getElementById('status').innerHTML = 'Please log into this app.';
    }
  }
  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }
  window.fbAsyncInit = function() {
    FB.init({
      appId : '1361583235948040',
      cookie : true,
      xfbml : true,
      version : 'v19.0'
    });
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  };
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));
  function testAPI() {
    FB.api('/me', function(response) {
      document.getElementById('status').innerHTML = 'Thanks for logging in, ' + response.name + '!';
    });
  }
</script>

<h1>MRBELE V3 ONLINE 24/7</h1>
<p>Instagram AutoDM Bot for @mvsventures (ID: 2243884129743778) & @mrbele1</p>

<fb:login-button scope="public_profile,email,instagram_basic,instagram_manage_messages,pages_messaging" onlogin="checkLoginState();">
</fb:login-button>

<div id="status"></div>

<p><a href="/privacy">Privacy Policy</a> | <a href="/terms">Terms</a> | <a href="/data-deletion">Data Deletion</a></p>
<p>Contact: manveer998829@gmail.com | App ID: 1361583235948040</p>

</body>
</html>
"""

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
                    reply=ask_llama(text,sender)
                    requests.post(f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}",
                    json={"recipient":{"id":sender},"message":{"text":reply}},timeout=10)
    except Exception as e: print(e)
    return jsonify({"status":"ok"}),200

@app.route('/privacy')
def privacy(): return "Privacy Policy: This app @mvsventures bot only reads Instagram DMs to auto-reply about services. No data stored. Contact: manveer998829@gmail.com"
@app.route('/terms')
def terms(): return "Terms: Business auto-reply only. Contact manveer998829@gmail.com"
@app.route('/data-deletion')
def deletion(): return "To delete data, DM 'DELETE MY DATA' or email manveer998829@gmail.com - Deleted in 24h"
if __name__=="__main__": app.run(host="0.0.0.0",port=10000)

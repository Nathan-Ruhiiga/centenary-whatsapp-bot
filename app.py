import os
import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    print("User message:", incoming_msg)  # 🔍 debug

    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg == 'menu':
        msg.body("🌟 Welcome... (menu text)")
    elif incoming_msg == '1':
        msg.body("Your balance is UGX...")
    # ... other fixed responses
    else:
        try:
            print("Calling GPT...")  # 🔍 debug
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful and professional Centenary Bank assistant."},
                    {"role": "user", "content": incoming_msg}
                ],
                temperature=0.4,
                max_tokens=300
            )
            reply = response['choices'][0]['message']['content'].strip()
            print("GPT reply:", reply)  # 🔍 debug
            msg.body(reply)
        except Exception as e:
            print("Error:", str(e))  # 🔍 debug
            msg.body("Sorry, something went wrong. Type 'menu'.")

    return str(resp)

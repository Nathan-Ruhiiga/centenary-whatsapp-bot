import os
import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Load your OpenAI API key (add this to Render environment later)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Predefined commands
    if incoming_msg == 'menu':
        msg.body(
            "🌟 Welcome to Centenary Bank!\n\n"
            "Please reply with an option:\n"
            "1. 📄 Check balance\n"
            "2. 🏦 Nearest ATM\n"
            "3. 💰 Loan calculator\n"
            "4. 🌍 Choose language\n"
            "5. 👨‍💼 Talk to an agent"
        )

    elif incoming_msg == '1':
        msg.body("💼 Your current balance is UGX 1,250,000.")

    elif incoming_msg == '2':
        msg.body("📍 The nearest Centenary ATM is at Bugolobi branch.")

    elif incoming_msg == '3':
        msg.body("💡 Please reply with your monthly income in UGX.")

    elif incoming_msg == '4':
        msg.body("🌍 Reply with your language:\n- `luganda`\n- `runyankole`\n- `english`")

    elif incoming_msg == '5':
        msg.body("👨‍💼 Connecting you to a Centenary agent... Please wait.")

    else:
        # Fallback to GPT
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful and professional virtual assistant for Centenary Bank in Uganda. Answer briefly and clearly."},
                    {"role": "user", "content": incoming_msg}
                ],
                temperature=0.4,
                max_tokens=300
            )
            reply = response['choices'][0]['message']['content'].strip()
            msg.body(reply)
        except Exception as e:
            msg.body("🤖 Sorry, I had trouble understanding that. Please try again or type `menu`.")

    return str(resp)

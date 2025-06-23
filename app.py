from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

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
        msg.body("💼 Your current balance is UGX 1,250,000. Is there anything else I can help with?")

    elif incoming_msg == '2':
        msg.body("📍 The nearest Centenary ATM is at Bugolobi branch, just 2km away from your location.")

    elif incoming_msg == '3':
        msg.body("💡 Please reply with your monthly income in UGX to check loan eligibility.")

    elif incoming_msg == '4':
        msg.body("🌍 Please reply with your preferred language:\n- `luganda`\n- `runyankole`\n- `english`")

    elif incoming_msg == '5':
        msg.body("👨‍💼 Connecting you to a Centenary agent... Please wait.")

    elif incoming_msg.isdigit():
        msg.body("🙁 I understood that as option " + incoming_msg + ", but it's not in the menu. Type `menu` to try again.")

    else:
        msg.body("🤖 Sorry, I didn't understand that. Type `menu` to start again.")

    return str(resp)

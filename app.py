from flask import Flask, request, jsonify
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg == 'menu':
        msg.body("Welcome to Centenary Bank! Choose:\n1. Balance\n2. Loan info\n3. Branch info\n4. Language\n5. Agent")
    else:
        msg.body("Sorry, I didn't understand. Type 'menu'.")

    return str(resp)

if __name__ == "__main__":
    app.run()

# Sample menu
menu_text = """Welcome to Centenary Bank! How can I help you today?
1. 📄 Account balance
2. 🏦 Nearest branch/ATM
3. 💰 Loan eligibility
4. 🗣️ Change language
5. 👨‍💼 Speak to a representative"""

@app.route("/", methods=["GET"])
def health_check():
    return "Centenary Bot API is running."

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming = request.get_json()
    message = incoming.get("Body", "").strip().lower()

    if message in ["hi", "hello", "menu"]:
        return respond(menu_text)
    elif message == "1":
        return respond("Please enter your account number (last 4 digits):")
    elif message == "1234":
        return respond("Your account balance is UGX 752,000 as of today.")
    elif message == "2":
        return respond("Your nearest ATM is at Centenary House, Entebbe Road.")
    elif message == "3":
        return respond("Please enter your monthly income (UGX):")
    elif message.isdigit():
        return respond("Based on your income, you may qualify for a Business Boost Loan. Our team will contact you shortly.")
    elif message == "4":
        return respond("Choose language: 1. English, 2. Luganda, 3. Runyankole")
    elif message == "5":
        return respond("Please hold. A representative will join shortly.")
    else:
        return respond("I'm sorry, I didn't understand that. Please type 'menu' to begin.")

def respond(message):
    return jsonify({"reply": message})

if __name__ == "__main__":
    app.run(debug=True)

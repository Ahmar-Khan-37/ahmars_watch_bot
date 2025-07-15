from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "ahmarverifytoken"

# Dummy Watch List (Update later)
watch_catalog = {
    "Rolex Submariner": "PKR 2,500,000",
    "Omega Seamaster": "PKR 850,000",
    "Casio Edifice": "PKR 25,000",
    "Tissot Classic": "PKR 150,000"
}

def greeting_message():
    return "Hello! خوش آمدید to Ahmar's Watches. Aapko kia chahiye? Watches, Prices ya Details?"

def list_watches():
    watches = "\n".join(watch_catalog.keys())
    return f"Available Watches:\n{watches}"

def get_watch_price(user_message):
    for watch in watch_catalog:
        if watch.lower() in user_message.lower():
            return f"{watch} ki price hai: {watch_catalog[watch]}"
    return "Kis watch ki price chahiye? Please name batain."

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return str(challenge)
        return "Verification token mismatch", 403

    data = request.get_json()
    print("Received message:", data)
    
    if 'message' in data:
        user_message = data['message'].get('text', '').lower()
        
        if any(word in user_message for word in ['hi', 'hello', 'salam', 'assalam']):
            reply = greeting_message()
        
        elif 'watch' in user_message or 'watches' in user_message:
            reply = list_watches()
        
        elif 'price' in user_message or 'qeemat' in user_message:
            reply = get_watch_price(user_message)
        
        else:
            reply = "Sorry, mai samajh nahi saka. Apko watches list chahiye, price ya koi or madad?"
        
        return jsonify({'reply': reply})

    return "No message found", 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)

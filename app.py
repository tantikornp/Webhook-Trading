import json, config
from flask import Flask, request, jsonify, render_template
import ccxt

myFTX = ccxt.ftx({
 'api_key': config.API_KEY,     # API Keys
 'secret': config.API_SECRET})  # API Secret

myFTX.headers = {
    'FTX-SUBACCOUNT': 'BotTrading',
} 

app = Flask(__name__)

def order(side, quantity, symbol, order_type = 'market'):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = myFTX.create_order(symbol = symbol, side = side, type = order_type, amount = quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')
    
@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request.data)
    data = json.loads(request.data)
    
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    side       = data['strategy']['order_action'].lower()
    quantity   = data['strategy']['order_contracts']
    symbol     = data['ticker'].upper()

    order_response = order(side, quantity, symbol)

    if order_response:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        return {
            "code": "error",
            "message": "order failed"
        }

if __name__ == '__main__':
    app.run(debug = True)
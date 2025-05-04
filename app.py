import os
import stripe
import json

from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

app = Flask(__name__,
  static_url_path='',
  template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
  static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))

def calculate_order_amount(amounts):
  total_amount = sum(float(amount) for amount in amounts.values())
  return int(total_amount)

# Home route
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

# Checkout route
@app.route('/checkout', methods=['GET'])
def checkout():
  # Just hardcoding amounts here to avoid using a database
  item = request.args.get('item')
  title = None
  amount = None
  error = None

  if item == '1':
    title = 'The Art of Doing Science and Engineering'
    amount = 2300
  elif item == '2':
    title = 'The Making of Prince of Persia: Journals 1985-1993'
    amount = 2500
  elif item == '3':
    title = 'Working in Public: The Making and Maintenance of Open Source'
    amount = 2800
  else:
    # Included in layout view, feel free to assign error
    error = 'No item selected'

  return render_template('checkout.html', title=title, amount=amount, error=error)

# Create Payment Intent Route
@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
  try:
    data = json.loads(request.data)
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=calculate_order_amount(data['items_price']),
        currency='sgd',
        # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
        automatic_payment_methods={
            'enabled': True,
        },
    )
    return jsonify({
        'clientSecret': intent['client_secret']

    })
  except Exception as e:
    return jsonify(error=str(e)), 403


# Success route
@app.route('/success', methods=['GET'])
def success():
  payment_intent_id = request.args.get('payment_intent')
  payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
  amount = payment_intent["amount"]
  return render_template('success.html', payment_intent_id=payment_intent_id, amount=amount)

if __name__ == '__main__':
  app.run(port=5000, host='0.0.0.0', debug=True)
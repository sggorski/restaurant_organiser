from flask import Flask, jsonify, render_template, request, url_for
from database import load_menu, load_order, save_order

app = Flask(__name__)

@app.route('/')
def home_view():
    return render_template('home.html')

@app.route('/order/')
def order():
    return render_template('order.html', food=load_menu())

@app.route("/order/submit", methods=['POST'])
def submit():
    data = request.form
    if len(data) == 0:
        return render_template('order.html', food=load_menu())
    data2 = load_order(list(data.keys()))
    total=0
    for item in data2:
        total+= item['price']
    return render_template('order_confirm.html', data=data2, total_price = total)

@app.route('/order/submit/confirmation', methods=['POST'])
def confirmation():
    data=request.form
    save_order(data)
    return render_template('confirmation.html', data=data)

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
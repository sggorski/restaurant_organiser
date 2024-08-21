from flask import Flask, jsonify, render_template, request, url_for
from database import load_menu, load_order, save_order, remove_meal, remove_order, load_current_orders, update_meal, add_meal
from mail import send_mail

app = Flask(__name__)

@app.route('/')
def home_view():
    return render_template('home.html')

@app.route('/order/')
def order():
    return render_template('order.html', food=load_menu())

@app.route('/edit/')
def edit():
    return render_template('edition.html', menu = load_menu())
    
@app.route('/orders/')
def orders():
    orders=load_current_orders(),
    orders_list = []
    for order in orders[0]: 
        ids_list = order['order_info'][:-1].split(',')
        orders_dict = {'id' : order['id'], 'order_info' : load_order(ids_list)}
        orders_list.append(orders_dict)
    return render_template('current_orders.html', orders = orders_list)


@app.route('/orders/', methods=['POST'])
def cancel_order():
    data = request.form
    remove_order(data['id'])
    return orders()

@app.route('/edit/', methods=['POST'])
def cancel_meal():
    data = request.form
    if len(data)==1:
        remove_meal(data['id'])
    elif data['id']=='-1':
        if data['description2'] == "":
            add_meal(data['name'], data['price'], data['description'])
        else:
            add_meal(data['name'], data['price'], data['description2'])
    else:
        if data['description'] ==  data['original_text']:
            update_meal(data['name'], data['price'], data['description2'], data['id'])
        else:
            update_meal(data['name'], data['price'], data['description'], data['id'])
    return edit()
    
@app.route('/edit/<id>')
def edit_meal(id):
    print(load_order([id])[0])
    return render_template('edit_meal.html', meal = load_order([id])[0])

@app.route('/edit/add')
def add_new_meal():
    return render_template('add_meal.html')

@app.route("/order/submit", methods=['POST'])
def submit():
    data = request.form
    if len(data) == 0:
        return render_template('order.html', food=load_menu())
    data2 = load_order(list(data.keys()))
    data1 = list(data.keys())
    total=0
    for item in data2:
        total+= item['price']

    return render_template('order_confirm.html', ids = data1, data=data2, total_price = total)

@app.route('/order/submit/confirmation', methods=['POST'])
def confirmation():
    data=request.form
    order_str = ""
    for item in data['data'][1:-1].replace(" ", "").split(','):
        order_str += item[1:-1] + ","
    save_order(order_str)
    return render_template('confirmation.html', data=data)

@app.route('/raport/')
def raport():
    return render_template('raport.html')

@app.route('/raport/confirmation', methods=['POST'])
def send_raport():
    data = request.form
    message= f"Date: {data['date']} \nRevenue: {data['revenue']} \nOther information: {data['comments']} \n"
    print(message)
    send_mail(''.join(message))
    return render_template('raport_confirm.html')
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
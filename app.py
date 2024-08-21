from flask import Flask, jsonify, render_template, request, url_for
from database import load_menu, load_order, save_order, remove_meal, remove_order, load_current_orders, update_meal, add_meal
from mail import send_mail
import ast
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
    orders=load_current_orders()
    orders_list = []
    for order in orders: 
        ids = order['order_info'][:-1].split(",")
        quantities = order['quantity_info'][:-1].split(",")
        list_of_meals=[]
        for i, id in enumerate(ids):
            name = load_order([id])[0]['name']
            order_details = {'id' : id, 'quantity' : quantities[i], 'name' : name}
            list_of_meals.append(order_details)
        order_dict = {'id' : order['id'], 'meals' : list_of_meals}
        orders_list.append(order_dict)
    return  render_template('current_orders.html', orders = orders_list)


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
    ids = [key for key in data.keys() if data[key] == "on" ]
    my_dict = {int(key) : int(data[f'quantity_{key}']) for key in ids}
    if len(ids) == 0:
        return render_template('order.html', food=load_menu())
    data2 = load_order(ids)
    total=0
    for item in data2:
        total += int(item['price'])*int(my_dict[int(item['id'])])

    return render_template('order_confirm.html', ids = ids, data=data2, quantity=my_dict,  total_price = total)

@app.route('/order/submit/confirmation', methods=['POST'])
def confirmation():
    data=request.form
    data = ast.literal_eval(data['quantity'])
    id_str = ""
    q_str = ""
    for item in data.keys():
        id_str += str(item) + ","
        q_str += str(data[item]) + ","
    save_order(id_str, q_str)
    return render_template('confirmation.html')

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
from  sqlalchemy import create_engine, text
import os

from werkzeug import datastructures
engine = create_engine(os.environ['DB_STR'])

def load_menu():
  with engine.connect() as conn:
    result = conn.execute(text("select * from menu"))
    data = []
    for row in result.mappings().all():
      data.append(dict(row))
    return data

def load_current_orders():
  with engine.connect() as conn:
    result = conn.execute(text("select * from orders"))
    data = []
    for row in result.mappings().all():
      data.append(dict(row))
    return data
  
def load_order(ids):
  str_ids = ""
  print(ids)
  for item in ids:
    str_ids += item + ","
  cmd = f"select * from menu where id in ({str_ids[:-1]})"
  with engine.connect() as conn:
    data = []
    result = conn.execute(text(cmd))
    for row in result.mappings().all():
      data.append(dict(row))
    return data

def save_order(data):
  cmd = "insert into orders (order_info) values (:info)"
  with engine.connect() as conn:
    conn.execute(text(cmd), {"info": data})
    conn.commit()

def remove_order(id):
  cmd = "delete from orders where id =:id"
  with engine.connect() as conn:
    conn.execute(text(cmd), {"id": id})
    conn.commit()

def remove_meal(id):
  cmd = "delete from menu where id =:id"
  with engine.connect() as conn:
    conn.execute(text(cmd), {"id": id})
    conn.commit()

def update_meal(data):
  cmd ="UPDATE menu SET name = :name, price = :price, description = :description WHERE id =:id;"
  with engine.connect() as conn:
    conn.execute(text(cmd), {"name" : data['name'], "price" : data['price'], "description" : data['description'], "id" : data['id']})
    conn.commit()

def add_meal(data):
  cmd ="insert into menu (name, price, description) values (:name, :price, :description)"
  with engine.connect() as conn:
    conn.execute(text(cmd), {"name" : data['name'], "price" : data['price'], "description" : data['description']})
    conn.commit()
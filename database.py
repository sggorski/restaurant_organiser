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

def load_order(ids):
  str_ids = ""
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
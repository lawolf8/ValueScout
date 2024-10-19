from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Reflect the tables from the database schema
users_table = Table('users', metadata, autoload_with=engine)
user_lists_table = Table('user_lists', metadata, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_target_data_to_db(user_id, list_name, items_prices):
    try:
        for item_name, item_data in items_prices.items():
            quantity, price = item_data['quantity'], item_data['price']
            new_list_entry = {
                "userid": user_id,
                "list_name": list_name,
                "item": item_name,
                "item_quantity": quantity,
                "item_cost": price
            }
            session.execute(user_lists_table.insert().values(new_list_entry))

        session.commit()
        print(f"List '{list_name}' added successfully for user {user_id}")

    except Exception as e:
        print(f"Error adding list to database: {e}")
        session.rollback()

# Test
if __name__ == "__main__":
    user_id = 1  
    list_name = "Target Shopping List"
    items_prices = {
        'Fairlife Lactose-Free Skim Milk - 52 fl oz': {'quantity': 2, 'price': 3.99},
        "Annie's Shells & White Cheddar Mac & Cheese": {'quantity': 7, 'price': 1.39}
    }
    add_target_data_to_db(user_id, list_name, items_prices)
    session.close()

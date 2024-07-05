import random
from faker import Faker
import mysql.connector
from mysql.connector import Error

def connect_to_database(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Predefined lists for realistic data
categories = ["Electronics", "Clothing", "Books", "Toys", "Food", "Home Appliances", "Beauty", "Sports", "Automotive", "Health"]
brands = ["Samsung", "Apple", "Sony", "Nike", "Adidas", "Puma", "LG", "Panasonic", "Lenovo", "Dell"]
carriers = ["FedEx", "UPS", "DHL", "USPS"]

def insert_users(cursor, fake, num_users=100):
    for _ in range(num_users):
        username = fake.user_name()
        password = fake.password()
        name = fake.name()
        email = fake.email()
        contact_number = fake.phone_number()
        address = fake.address()
        cursor.execute("""
            INSERT INTO Users (username, password, name, email, contact_number, address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, password, name, email, contact_number, address))

def insert_managers(cursor, fake, num_managers=10):
    for _ in range(num_managers):
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        cursor.execute("""
            INSERT INTO Managers (username, password, email)
            VALUES (%s, %s, %s)
        """, (username, password, email))

def insert_categories(cursor, categories):
    for category in categories:
        cursor.execute("""
            INSERT INTO Categories (name)
            VALUES (%s)
        """, (category,))

def insert_brands(cursor, brands):
    for brand in brands:
        status = random.choice(['active', 'inactive', 'old'])
        cursor.execute("""
            INSERT INTO Brands (name, status)
            VALUES (%s, %s)
        """, (brand, status))

def insert_products(cursor, fake, categories, brands, num_products=100):
    for _ in range(num_products):
        name = fake.word().capitalize()
        description = fake.text()
        price = round(random.uniform(10, 1000), 2)
        stock = random.randint(0, 100)
        category_id = random.randint(1, len(categories))
        brand_id = random.randint(1, len(brands))
        status = random.choice(['active', 'inactive'])
        cursor.execute("""
            INSERT INTO Products (name, description, price, stock, category_id, brand_id, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, description, price, stock, category_id, brand_id, status))

def insert_shipping_info(cursor, fake, carriers, num_shipping_infos=50):
    for _ in range(num_shipping_infos):
        tracking_number = fake.uuid4()
        carrier = random.choice(carriers)
        shipping_date = fake.date_between(start_date='-1y', end_date='today')
        delivery_date = fake.date_between(start_date=shipping_date, end_date='+1w')
        status = random.choice(['pending', 'shipped', 'delivered', 'returned'])
        cursor.execute("""
            INSERT INTO ShippingInfo (tracking_number, carrier, shipping_date, delivery_date, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (tracking_number, carrier, shipping_date, delivery_date, status))

def insert_orders(cursor, fake, num_orders=100):
    for _ in range(num_orders):
        user_id = random.randint(1, 100)
        status = random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled', 'returned'])
        total_amount = round(random.uniform(20, 2000), 2)
        shipping_info_id = random.randint(1, 50)
        cursor.execute("""
            INSERT INTO Orders (user_id, status, total_amount, shipping_info_id)
            VALUES (%s, %s, %s, %s)
        """, (user_id, status, total_amount, shipping_info_id))

def insert_order_details(cursor, num_order_details=200):
    for _ in range(num_order_details):
        order_id = random.randint(1, 100)
        product_id = random.randint(1, 100)
        quantity = random.randint(1, 5)
        price = round(random.uniform(10, 1000), 2)
        cursor.execute("""
            INSERT INTO OrderDetails (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, product_id, quantity, price))

def insert_shopping_carts(cursor, num_carts=50):
    for _ in range(num_carts):
        user_id = random.randint(1, 100)
        cursor.execute("""
            INSERT INTO ShoppingCart (user_id)
            VALUES (%s)
        """, (user_id,))

def insert_cart_items(cursor, num_cart_items=100):
    for _ in range(num_cart_items):
        cart_id = random.randint(1, 50)
        product_id = random.randint(1, 100)
        quantity = random.randint(1, 5)
        cursor.execute("""
            INSERT INTO CartItems (cart_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (cart_id, product_id, quantity))

def insert_purchase_history(cursor, num_histories=100):
    for _ in range(num_histories):
        user_id = random.randint(1, 100)
        order_id = random.randint(1, 100)
        cursor.execute("""
            INSERT INTO PurchaseHistory (user_id, order_id)
            VALUES (%s, %s)
        """, (user_id, order_id))

def insert_comments(cursor, fake, num_comments=100):
    for _ in range(num_comments):
        product_id = random.randint(1, 100)
        user_id = random.randint(1, 100)
        comment = fake.text()
        status = random.choice(['approved', 'inappropriate'])
        moderated_by = random.randint(1, 10)
        cursor.execute("""
            INSERT INTO Comments (product_id, user_id, comment, status, moderated_by)
            VALUES (%s, %s, %s, %s, %s)
        """, (product_id, user_id, comment, status, moderated_by))

def insert_discounts(cursor, fake, num_discounts=10):
    for _ in range(num_discounts):
        name = fake.word().capitalize()
        description = fake.text()
        discount_percentage = round(random.uniform(5, 50), 2)
        start_date = fake.date_between(start_date='-1y', end_date='today')
        end_date = fake.date_between(start_date=start_date, end_date='+1m')
        cursor.execute("""
            INSERT INTO Discounts (name, description, discount_percentage, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, description, discount_percentage, start_date, end_date))

def insert_product_discounts(cursor, num_product_discounts=50):
    for _ in range(num_product_discounts):
        product_id = random.randint(1, 100)
        discount_id = random.randint(1, 10)
        cursor.execute("""
            INSERT INTO ProductDiscounts (product_id, discount_id)
            VALUES (%s, %s)
        """, (product_id, discount_id))

def main():
    conn = connect_to_database()
    cursor = conn.cursor()
    fake = Faker()

    insert_users(cursor, fake)
    insert_managers(cursor, fake)
    insert_categories(cursor, categories)
    insert_brands(cursor, brands)
    insert_products(cursor, fake, categories, brands)
    insert_shipping_info(cursor, fake, carriers)
    insert_orders(cursor, fake)
    insert_order_details(cursor)
    insert_shopping_carts(cursor)
    insert_cart_items(cursor)
    insert_purchase_history(cursor)
    insert_comments(cursor, fake)
    insert_discounts(cursor, fake)
    insert_product_discounts(cursor)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

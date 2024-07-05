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

def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        print("Query executed successfully")
    except Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        cursor.close()

def fetch_results(connection, query, params=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()

def fetch_one_result(connection, query, params=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    except Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()

# Connect to the database
connection = connect_to_database("your_host", "your_user", "your_password", "your_database")

# Query 1: List all inactive brands and the number of their products.
def list_inactive_brands_and_product_count(connection):
    query = """
    SELECT b.name AS brand , COUNT(p.product_id) AS product_count
    FROM Brands b
    JOIN Products p ON b.brand_id = p.brand_id
    WHERE b.status = 'inactive'
    GROUP BY b.name;
    """
    return fetch_results(connection, query)

# Query 2: Retrieve all users who registered in the last specified number of days.
def get_recent_users(connection, interval_days):
    query = """
    SELECT username, email, registration_date
    FROM Users
    WHERE registration_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY);
    """
    params = (interval_days,)
    return fetch_results(connection, query, params)

# Query 3: Get all products along with their category names.
def get_products_with_categories(connection):
    query = """
    SELECT p.name AS product_name, c.name AS category_name
    FROM Products p
    JOIN Categories c ON p.category_id = c.category_id;
    """
    return fetch_results(connection, query)

# Query 4: Find all orders placed by a specific user (given user_id) and their total amounts.
def get_orders_by_user(connection, user_id):
    query = """
    SELECT o.order_id, o.order_date, o.total_amount
    FROM Orders o
    WHERE o.user_id = %s;
    """
    params = (user_id,)
    return fetch_results(connection, query, params)

# Query 5: Get the details of products that have more than the specified number of units in stock.
def get_high_stock_products(connection, min_stock):
    query = """
    SELECT name, description, price, stock
    FROM Products
    WHERE stock > %s;
    """
    params = (min_stock,)
    return fetch_results(connection, query, params)

# Query 6: List the details of all orders and their shipping information.
def get_orders_with_shipping_info(connection):
    query = """
    SELECT o.order_id, o.order_date, o.status, s.tracking_number, s.carrier, s.shipping_date, s.delivery_date
    FROM Orders o
    JOIN ShippingInfo s ON o.shipping_info_id = s.shipping_info_id;
    """
    return fetch_results(connection, query)

# Query 7: Find all users who have made a purchase and the total amount they have spent.
def get_users_total_spent(connection):
    query = """
    SELECT u.user_id, u.username, SUM(o.total_amount) AS total_spent
    FROM Users u
    JOIN Orders o ON u.user_id = o.user_id
    GROUP BY u.user_id, u.username;
    """
    return fetch_results(connection, query)

# Query 8: Retrieve all approved comments for a specific product (given product_id).
def get_approved_comments_for_product(connection, product_id):
    query = """
    SELECT c.comment, c.comment_date, u.username
    FROM Comments c
    JOIN Users u ON c.user_id = u.user_id
    WHERE c.product_id = %s AND c.status = 'approved';
    """
    params = (product_id,)
    return fetch_results(connection, query, params)

# Query 9: Get all products along with their discounts, if any.
def get_products_with_discounts(connection):
    query = """
    SELECT p.name AS product_name, d.name AS discount_name, d.discount_percentage
    FROM Products p
    LEFT JOIN ProductDiscounts pd ON p.product_id = pd.product_id
    LEFT JOIN Discounts d ON pd.discount_id = d.discount_id;
    """
    return fetch_results(connection, query)

# Query 10: Retrieve the total number of products in each category.
def get_product_count_by_category(connection):
    query = """
    SELECT c.name AS category_name, COUNT(p.product_id) AS product_count
    FROM Categories c
    JOIN Products p ON c.category_id = p.category_id
    GROUP BY c.name;
    """
    return fetch_results(connection, query)


# Close the connection 
connection.close()

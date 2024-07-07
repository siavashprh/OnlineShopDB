import mysql.connector
from mysql.connector import Error
from pprint import pprint

HOST_NAME = "127.0.0.1"
USER = "root"
PASSWORD = "si@9833015"
DATABASE = "onlineshop"

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=HOST_NAME,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            auth_plugin="mysql_native_password"
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Execute a non-select query
def execute_query(connection, query, params=None):
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor.rowcount
    except Error as e:
        print(f"The error '{e}' occurred")

# Execute a select query
def execute_select_query(connection, query, params=None):
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"The error '{e}' occurred")

# Query 1: List all inactive brands and the number of their products
def list_inactive_brands_and_product_count(connection):
    query = """
    SELECT b.name AS brand , COUNT(p.product_id) AS product_count
    FROM Brands b
    JOIN Products p ON b.brand_id = p.brand_id
    WHERE b.status = 'inactive'
    GROUP BY b.name;
    """
    return execute_select_query(connection, query)

# Query 2: Retrieve all users who registered in the last specified number of days
def get_recent_users(connection, interval_days):
    query = """
    SELECT username, email, registration_date
    FROM Users
    WHERE registration_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY);
    """
    params = (interval_days,)
    return execute_select_query(connection, query, params)

# Query 3: Get all products along with their category names
def get_products_with_categories(connection):
    query = """
    SELECT p.name AS product_name, c.name AS category_name
    FROM Products p
    JOIN Categories c ON p.category_id = c.category_id;
    """
    return execute_select_query(connection, query)

# Query 4: Find all orders placed by a specific user (given user_id) and their total amounts
def get_orders_by_user(connection, user_id):
    query = """
    SELECT o.order_id, o.order_date, o.total_amount
    FROM Orders o
    WHERE o.user_id = %s;
    """
    params = (user_id,)
    return execute_select_query(connection, query, params)

# Query 5: Get the details of products that have more than the specified number of units in stock
def get_high_stock_products(connection, min_stock):
    query = """
    SELECT name, description, price, stock
    FROM Products
    WHERE stock > %s;
    """
    params = (min_stock,)
    return execute_select_query(connection, query, params)

# Query 6: List the details of all orders and their shipping information
def get_orders_with_shipping_info(connection):
    query = """
    SELECT o.order_id, o.order_date, o.status, s.tracking_number, s.carrier, s.shipping_date, s.delivery_date
    FROM Orders o
    JOIN ShippingInfo s ON o.shipping_info_id = s.shipping_info_id;
    """
    return execute_select_query(connection, query)

# Query 7: Find all users who have made a purchase and the total amount they have spent
def get_users_total_spent(connection):
    query = """
    SELECT u.user_id, u.username, SUM(o.total_amount) AS total_spent
    FROM Users u
    JOIN Orders o ON u.user_id = o.user_id
    GROUP BY u.user_id, u.username;
    """
    return execute_select_query(connection, query)

# Query 8: Retrieve all approved comments for a specific product (given product_id)
def get_approved_comments_for_product(connection, product_id):
    query = """
    SELECT c.comment, c.comment_date, u.username
    FROM Comments c
    JOIN Users u ON c.user_id = u.user_id
    WHERE c.product_id = %s AND c.status = 'approved';
    """
    params = (product_id,)
    return execute_select_query(connection, query, params)

# Query 9: Get all products along with their discounts, if any
def get_products_with_discounts(connection):
    query = """
    SELECT p.name AS product_name, d.name AS discount_name, d.discount_percentage
    FROM Products p
    LEFT JOIN ProductDiscounts pd ON p.product_id = pd.product_id
    LEFT JOIN Discounts d ON pd.discount_id = d.discount_id;
    """
    return execute_select_query(connection, query)

# Query 10: Retrieve the total number of products in each category
def get_product_count_by_category(connection):
    query = """
    SELECT c.name AS category_name, COUNT(p.product_id) AS product_count
    FROM Categories c
    JOIN Products p ON c.category_id = p.category_id
    GROUP BY c.name;
    """
    return execute_select_query(connection, query)

# Main function to interactively choose and execute queries
if __name__ == "__main__":
    connection = create_connection()
    if connection:
        while True:
            print("\nChoose a query to execute:")
            print("1. List all inactive brands and the number of their products.")
            print("2. Retrieve all users who registered in the last specified number of days.")
            print("3. Get all products along with their category names.")
            print("4. Find all orders placed by a specific user (given user_id) and their total amounts.")
            print("5. Get the details of products that have more than the specified number of units in stock.")
            print("6. List the details of all orders and their shipping information.")
            print("7. Find all users who have made a purchase and the total amount they have spent.")
            print("8. Retrieve all approved comments for a specific product (given product_id).")
            print("9. Get all products along with their discounts, if any.")
            print("10. Retrieve the total number of products in each category.")
            print("0. Exit")

            choice = input("Enter the number of the query you want to execute: ")

            if choice == '1':
                results = list_inactive_brands_and_product_count(connection)
                print("Inactive brands and their product counts:")
                pprint(results)

            elif choice == '2':
                interval_days = int(input("Enter the number of days: "))
                results = get_recent_users(connection, interval_days)
                print("Recent users:")
                pprint(results)

            elif choice == '3':
                results = get_products_with_categories(connection)
                print("Products with their categories:")
                pprint(results)

            elif choice == '4':
                user_id = int(input("Enter the user_id: "))
                results = get_orders_by_user(connection, user_id)
                print("Orders placed by the user:")
                pprint(results)

            elif choice == '5':
                min_stock = int(input("Enter the minimum stock: "))
                results = get_high_stock_products(connection, min_stock)
                print("Products with high stock:")
                pprint(results)

            elif choice == '6':
                results = get_orders_with_shipping_info(connection)
                print("Orders with their shipping information:")
                pprint(results)

            elif choice == '7':
                results = get_users_total_spent(connection)
                print("Users who have made a purchase and their total spent amounts:")
                pprint(results)

            elif choice == '8':
                product_id = int(input("Enter the product_id: "))
                results = get_approved_comments_for_product(connection, product_id)
                print("Approved comments for the product:")
                pprint(results)

            elif choice == '9':
                results = get_products_with_discounts(connection)
                print("Products with their discounts:")
                pprint(results)

            elif choice == '10':
                results = get_product_count_by_category(connection)
                print("Product counts by category:")
                pprint(results)

            elif choice == '0':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

        connection.close()
        print("Connection closed")

import subprocess as sp
import pymysql
import pymysql.cursors
import sys

# Global variables for database connection
con = None
cur = None

def seller_menu(seller_id):
    """
    Menu for Seller-specific functions.
    """
    while True:
        tmp = sp.call('clear', shell=True)
        print(f"Seller Menu (Seller ID: {seller_id})")
        print("1. Add or Update Product")
        print("2. Delete Product")
        print("3. Add Product Image")
        print("4. Delete Product Image")
        print("5. Add Promotion")
        print("6. Delete Promotion")
        print("7. View Product Reviews")
        print("8. Logout")

        choice = int(input("Enter choice> "))
        tmp = sp.call('clear', shell=True)

        if choice == 1:
            add_or_update_product(seller_id)
        elif choice == 2:
            delete_product(seller_id)
        elif choice == 3:
            add_product_image(seller_id)
        elif choice == 4:
            delete_product_image(seller_id)
        elif choice == 5:
            add_promotion(seller_id)
        elif choice == 6:
            delete_promotion(seller_id)
        elif choice == 7:
            view_product_reviews(seller_id)
        elif choice == 8:
            return
        else:
            print("Invalid option. Try again.")
            input("Press Enter to continue...")


def buyer_menu(customer_id):
    """
    Menu for Buyer-specific functions.
    """
    while True:
        tmp = sp.call('clear', shell=True)
        print(f"Customer Menu (Customer ID: {customer_id})")
        print("1. View Products")
        print("2. View Product Reviews")
        print("3. View Seller Details")
        print("4. View Orders")
        print("5. View Product Images")
        print("6. View Promotions")
        print("7. Logout")

        choice = int(input("Enter choice> "))
        tmp = sp.call('clear', shell=True)

        if choice == 1:
            view_products()
        elif choice == 2:
            view_product_reviews()
        elif choice == 3:
            view_seller_details()
        elif choice == 4:
            view_orders(customer_id)
        elif choice == 5:
            view_product_images()
        elif choice == 6:
            view_promotions()
        elif choice == 7:
            return
        else:
            print("Invalid option. Try again.")
            input("Press Enter to continue...")


def manager_menu():
    """
    Menu for Manager-specific functions.
    """
    while True:
        tmp = sp.call('clear', shell=True)
        print("Manager Menu")
        print("1. Update Customer Details")
        print("2. Update Seller Details")
        print("3. Add/Update Premium Seller Tier")
        print("4. Update Discount Codes")
        print("5. Update Promotions")
        print("6. View Total Sales by Category")
        print("7. Logout")

        choice = int(input("Enter choice> "))
        tmp = sp.call('clear', shell=True)

        if choice == 1:
            update_customer_details()
        elif choice == 2:
            update_seller_details()
        elif choice == 3:
            add_or_update_premium_seller()
        elif choice == 4:
            update_discount_codes()
        elif choice == 5:
            update_promotions()
        elif choice == 6:
            view_sales_statistics()
        elif choice == 7:
            return
        else:
            print("Invalid option. Try again.")
            input("Press Enter to continue...")


def main_menu():
    """
    Main menu to select user type.
    """
    while True:
        tmp = sp.call('clear', shell=True)
        print("Welcome to the Online Marketplace Management System")
        print("1. Seller")
        print("2. Customer")
        print("3. Manager")
        print("4. Exit")

        choice = int(input("Enter choice> "))
        tmp = sp.call('clear', shell=True)

        if choice == 1:
            while True:
                seller_id = input("Enter Seller ID (or type 'back' to return to main menu): ")
                if seller_id.lower() == 'back':
                    break
                # Check if seller ID exists
                query = "SELECT * FROM Seller WHERE seller_id = %s;"
                cur.execute(query, (seller_id,))
                seller = cur.fetchone()
                if seller:
                    seller_menu(seller_id)
                    break
                else:
                    print("Invalid Seller ID. Please try again.")
        elif choice == 2:
            while True:
                customer_id = input("Enter Customer ID (or type 'back' to return to main menu): ")
                if customer_id.lower() == 'back':
                    break
                # Check if customer ID exists
                query = "SELECT * FROM Customer WHERE customer_id = %s;"
                cur.execute(query, (customer_id,))
                customer = cur.fetchone()
                if customer:
                    buyer_menu(customer_id)
                    break
                else:
                    print("Invalid Customer ID. Please try again.")
        elif choice == 3:
            password = input("Enter Manager Password: ")
            if password == "managerpass":
                manager_menu()
            else:
                print("Invalid password. Access denied.")
                input("Press Enter to continue...")

        elif choice == 4:
            print("Exiting the system. Goodbye!")
            exit()
        else:
            print("Invalid option. Try again.")
            input("Press Enter to continue...")


# Helper functions for various operations
def add_or_update_product(seller_id):
    """
    Add or update a product for a seller.
    """
    try:
        row = {}
        print(f"Adding or Updating Product for Seller ID: {seller_id}")
        row["product_id"] = input("Product ID: ")
        row["SKU"] = input("SKU: ")
        row["name"] = input("Name: ")
        row["price"] = float(input("Price: "))
        row["stock"] = int(input("Stock: "))
        row["category_id"] = input("Category ID: ")

        query = f"""
        INSERT INTO Product (product_id, SKU, name, price, stock, seller_id, category_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        name = %s, price = %s, stock = %s, category_id = %s;
        """
        cur.execute(query, (
            row["product_id"], row["SKU"], row["name"], row["price"], row["stock"], seller_id, row["category_id"],
            row["name"], row["price"], row["stock"], row["category_id"]
        ))
        con.commit()
        print("Product added/updated successfully.")

    except Exception as e:
        con.rollback()
        print("Failed to add/update product.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def delete_product(seller_id):
    """
    Delete a product for a seller.
    """
    try:
        product_id = input("Enter Product ID to delete: ")
        SKU_id = input("Enter SKU ID to delete: ")
        # Check if the product exists and belongs to the seller
        query_check = "SELECT * FROM Product WHERE product_id = %s AND SKU = %s AND seller_id = %s;"
        cur.execute(query_check, (product_id, SKU_id, seller_id))
        product = cur.fetchone()
        if not product:
            print("Product not found or does not belong to you.")
            input("Press Enter to continue...")
            return

        # Delete the product
        query_delete = "DELETE FROM Product WHERE product_id = %s AND SKU = %s AND seller_id = %s;"
        cur.execute(query_delete, (product_id, SKU_id, seller_id))
        con.commit()

        print("Product deleted successfully.")
        input("Press Enter to continue...")

    except Exception as e:
        con.rollback()
        print("Failed to delete product.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def add_product_image(seller_id):
    """
    Add an image for one of the seller's products.
    """
    try:
        product_id = input("Enter Product ID: ")
        # Check if the product belongs to the seller
        query_check = "SELECT * FROM Product WHERE product_id = %s AND seller_id = %s;"
        cur.execute(query_check, (product_id, seller_id))
        product = cur.fetchone()
        if not product:
            print("Product not found or does not belong to you.")
            input("Press Enter to continue...")
            return
        # Get image path from user
        image_path = input("Enter the path to the image file: ")
        # Read the image file
        with open(image_path, 'rb') as file:
            image_data = file.read()
        # Insert into Product_Images
        query_insert = "INSERT INTO Product_Images (product_id, image) VALUES (%s, %s);"
        cur.execute(query_insert, (product_id, image_data))
        con.commit()
        print("Product image added successfully.")
        input("Press Enter to continue...")
    except Exception as e:
        con.rollback()
        print("Failed to add product image.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def delete_product_image(seller_id):
    """
    Delete an image for one of the seller's products.
    """
    try:
        product_id = input("Enter Product ID: ")
        # Check if the product belongs to the seller
        query_check = "SELECT * FROM Product WHERE product_id = %s AND seller_id = %s;"
        cur.execute(query_check, (product_id, seller_id))
        product = cur.fetchone()
        if not product:
            print("Product not found or does not belong to you.")
            input("Press Enter to continue...")
            return
        # Show available images for the product
        query_images = "SELECT image_id FROM Product_Images WHERE product_id = %s;"
        cur.execute(query_images, (product_id,))
        images = cur.fetchall()
        if not images:
            print("No images found for this product.")
            input("Press Enter to continue...")
            return
        print("Available images for this product:")
        for img in images:
            print(f"Image ID: {img['image_id']}")
        image_id = int(input("Enter the Image ID to delete: "))
        # Delete the image
        query_delete = "DELETE FROM Product_Images WHERE image_id = %s AND product_id = %s;"
        cur.execute(query_delete, (image_id, product_id))
        con.commit()
        print("Product image deleted successfully.")
        input("Press Enter to continue...")
    except Exception as e:
        con.rollback()
        print("Failed to delete product image.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def add_promotion(seller_id):
    """
    Add a promotion.
    """
    try:
        promotion_id = input("Enter Promotion ID: ")
        type = input("Enter Promotion type: ")
        start_date = input("Enter Start Date (YYYY-MM-DD): ")
        end_date = input("Enter End Date (YYYY-MM-DD): ")
        amount = input("Enter Amount: ")

        query_insert = """
        INSERT INTO Promotion (promotion_id, type, start_date, end_date, discount_amount, provided_by)
        VALUES (%s, %s, %s, %s , %s, %s);
        """
        cur.execute(query_insert, (promotion_id, type, start_date, end_date, amount, seller_id))
        con.commit()
        print("Promotion added successfully.")
        input("Press Enter to continue...")
    except Exception as e:
        con.rollback()
        print("Failed to add promotion.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def delete_promotion(seller_id):
    """
    Delete a promotion associated with the seller.
    """
    try:
        promotion_id = input("Enter Promotion ID to delete: ")

        # Check if the promotion exists and is associated with the seller
        query_check = """
        SELECT * FROM Promotion WHERE promotion_id = %s AND seller_id = %s;
        """
        cur.execute(query_check, (promotion_id, seller_id))
        promotion = cur.fetchone()
        if not promotion:
            print("Promotion not found or does not belong to you.")
            input("Press Enter to continue...")
            return

        # Delete the promotion
        query_delete = "DELETE FROM Promotion WHERE promotion_id = %s;"
        cur.execute(query_delete, (promotion_id,))
        con.commit()

        print("Promotion deleted successfully.")
        input("Press Enter to continue...")
    except Exception as e:
        con.rollback()
        print("Failed to delete promotion.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def view_product_reviews(seller_id=None):
    """
    View reviews for products.
    """
    try:
        if seller_id:
            # Seller wants to view reviews for their products
            # Get all products for the seller
            query_products = "SELECT product_id, name FROM Product WHERE seller_id = %s;"
            cur.execute(query_products, (seller_id,))
            products = cur.fetchall()
            if not products:
                print("No products found for this seller.")
                input("Press Enter to continue...")
                return
            print("Your Products:")
            for product in products:
                print(f"Product ID: {product['product_id']}, Name: {product['name']}")
            # Ask seller if they want to view reviews for a specific product
            product_id = input("Enter Product ID to view reviews (or press Enter to view reviews for all products): ")
            if product_id:
                query_reviews = """
                SELECT pr.review_id, pr.customer_id, pr.rating, pr.comment, pr.review_date
                FROM Product_Review pr
                WHERE pr.product_id = %s;
                """
                cur.execute(query_reviews, (product_id,))
                reviews = cur.fetchall()
                if not reviews:
                    print("No reviews found for this product.")
                    input("Press Enter to continue...")
                    return
                print("Product Reviews:")
                for review in reviews:
                    print(f"Review ID: {review['review_id']}, Customer ID: {review['customer_id']}, Rating: {review['rating']}, Comment: {review['comment']}, Date: {review['review_date']}")
            else:
                print("No reviews found.")
                input("Press Enter to continue...")
                return
        else:
            # Buyer wants to view reviews for a product
            product_id = input("Enter Product ID to view reviews: ")
            query_reviews = """
            SELECT pr.review_id, pr.customer_id, pr.rating, pr.comment, pr.review_date
            FROM Product_Review pr
            WHERE pr.product_id = %s;
            """
            cur.execute(query_reviews, (product_id,))
            reviews = cur.fetchall()
            if not reviews:
                print("No reviews found for this product.")
                input("Press Enter to continue...")
                return
            print("Product Reviews:")
            for review in reviews:
                print(f"Review ID: {review['review_id']}, Customer ID: {review['customer_id']}, Rating: {review['rating']}, Comment: {review['comment']}, Date: {review['review_date']}")
        input("Press Enter to continue...")
    except Exception as e:
        print("Failed to retrieve product reviews.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def view_products():
    """
    View all products available in the marketplace.
    """
    try:
        query = "SELECT * FROM Product;"
        cur.execute(query)
        results = cur.fetchall()
        print("Available Products:")
        for row in results:
            print(f"Product ID: {row['product_id']}, Name: {row['name']}, Price: {row['price']}, Stock: {row['stock']}, Seller ID: {row['seller_id']}, Category ID: {row['category_id']}")
        input("Press Enter to continue...")

    except Exception as e:
        print("Failed to retrieve products.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def view_seller_details():
    """
    View details about a seller.
    """
    try:
        seller_id = input("Enter Seller ID to view details: ")
        query_seller = """
        SELECT s.seller_id, s.name, s.street, s.city, s.state, s.zip, s.join_date, s.rating
        FROM Seller s
        WHERE s.seller_id = %s;
        """
        cur.execute(query_seller, (seller_id,))
        seller = cur.fetchone()
        if not seller:
            print("Seller not found.")
            input("Press Enter to continue...")
            return
        print("Seller Details:")
        print(f"Seller ID: {seller['seller_id']}")
        print(f"Name: {seller['name']}")
        print(f"Address: {seller['city']}, {seller['state']}, {seller['zip']}")
        print(f"Rating: {seller['rating']}")
        # Check if the seller is a premium seller
        query_premium = "SELECT * FROM Premium_Seller WHERE seller_id = %s;"
        cur.execute(query_premium, (seller_id,))
        premium = cur.fetchone()
        if premium:
            print(f"Premium Seller since: {premium['premium_since']}")
            print(f"Tier: {premium['tier']}")
        input("Press Enter to continue...")
    except Exception as e:
        print("Failed to retrieve seller details.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def view_orders(customer_id):
    """
    View orders for the customer.
    """
    try:
        query_orders = """
        SELECT o.order_id, o.transaction_id, o.rating, o.order_date, o.order_status
        FROM Orders o
        WHERE o.ordered_by = %s;
        """
        cur.execute(query_orders, (customer_id,))
        orders = cur.fetchall()
        if not orders:
            print("No orders found for this customer.")
            input("Press Enter to continue...")
            return
        print("Your Orders:")
        for order in orders:
            print(f"Order ID: {order['order_id']}, Transaction ID: {order['transaction_id']}, Order Date: {order['order_date']}, Status: {order['order_status']}")
            # Optionally, display order items
            query_items = """
            SELECT oi.item_number, oi.product_id, oi.quantity, oi.unit_price
            FROM Order_Item oi
            WHERE oi.order_id = %s;
            """
            cur.execute(query_items, (order['order_id'],))
            items = cur.fetchall()
            for item in items:
                print(f"    Product ID: {item['product_id']}, Quantity: {item['quantity']}, Unit Price: {item['unit_price']}")
        input("Press Enter to continue...")
    except Exception as e:
        print("Failed to retrieve orders.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def view_product_images():
    """
    View images for a product.
    """
    try:
        product_id = input("Enter Product ID to view images: ")
        query_images = "SELECT image_id, image FROM Product_Images WHERE product_id = %s;"
        cur.execute(query_images, (product_id,))
        images = cur.fetchall()
        if not images:
            print("No images found for this product.")
            input("Press Enter to continue...")
            return
        print("Product Images:")
        for idx, img in enumerate(images):
            # For simplicity, we will simply print the blob data
            print(f"Image ID: {img['image_id']}, Image Data: {img['image'][:20]}...")
        input("Press Enter to continue...")
    except Exception as e:
        print("Failed to retrieve product images.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def view_promotions():
    """
    View current promotions and discount codes.
    """
    try:
        query_promotions = """
        SELECT code, type, value, expiry
        FROM Discount_Code
        WHERE expiry >= CURDATE();
        """
        cur.execute(query_promotions)
        promotions = cur.fetchall()
        if not promotions:
            print("No current promotions or discount codes available.")
            input("Press Enter to continue...")
            return
        print("Available Promotions and Discount Codes:")
        for promo in promotions:
            print(f"Code: {promo['code']}, Type: {promo['type']}, Value: {promo['value']}, Expiry: {promo['expiry']}")
        input("Press Enter to continue...")
    except Exception as e:
        print("Failed to retrieve promotions.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def update_customer_details():
    """
    Update details of a customer.
    """
    try:
        customer_id = input("Enter Customer ID to update: ")
        # Fetch current details
        query_customer = "SELECT * FROM Customer WHERE customer_id = %s;"
        cur.execute(query_customer, (customer_id,))
        customer = cur.fetchone()
        if not customer:
            print("Customer not found.")
            input("Press Enter to continue...")
            return
        print("Current Details:")
        for key, value in customer.items():
            print(f"{key}: {value}")
        # Get new details
        print("Enter new details (leave blank to keep current value):")
        name = input(f"Name [{customer['name']}]: ") or customer['name']
        email = input(f"Email [{customer['email']}]: ") or customer['email']
        street = input(f"Street [{customer['street']}]: ") or customer['street']
        city = input(f"City [{customer['city']}]: ") or customer['city']
        state = input(f"State [{customer['state']}]: ") or customer['state']
        zip_code = input(f"Zip [{customer['zip']}]: ") or customer['zip']
        # Update the customer
        query_update = """
        UPDATE Customer
        SET name = %s, email = %s, street = %s, city = %s, state = %s, zip = %s
        WHERE customer_id = %s;
        """
        cur.execute(query_update, (name, email, street, city, state, zip_code, customer_id))
        con.commit()
        print("Customer details updated successfully.")
        input("Press Enter to continue...")
    except Exception as e:
        con.rollback()
        print("Failed to update customer details.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def update_seller_details():
    """
    Update details of a seller.
    """
    try:
        seller_id = input("Enter Seller ID to update: ")
        # Fetch current details
        query_seller = "SELECT * FROM Seller WHERE seller_id = %s;"
        cur.execute(query_seller, (seller_id,))
        seller = cur.fetchone()
        if not seller:
            print("Seller not found.")
            input("Press Enter to continue...")
            return
        print("Current Details:")
        for key, value in seller.items():
            print(f"{key}: {value}")
        # Get new details
        print("Enter new details (leave blank to keep current value):")
        name = input(f"Name [{seller['name']}]: ") or seller['name']
        street = input(f"Street [{seller['street']}]: ") or seller['street']
        city = input(f"City [{seller['city']}]: ") or seller['city']
        state = input(f"State [{seller['state']}]: ") or seller['state']
        zip_code = input(f"Zip [{seller['zip']}]: ") or seller['zip']
        rating = input(f"Rating [{seller['rating']}]: ") or seller['rating']
        # Update the seller
        query_update = """
        UPDATE Seller
        SET name = %s, street = %s, city = %s, state = %s, zip = %s, rating = %s
        WHERE seller_id = %s;
        """
        cur.execute(query_update, (name, street, city, state, zip_code, rating, seller_id))
        con.commit()
        print("Seller details updated successfully.")
        input("Press Enter to continue...")
    except Exception as e:
        con.rollback()
        print("Failed to update seller details.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def add_or_update_premium_seller():
    """
    Add a seller to premium seller or update their tier.
    """
    try:
        seller_id = input("Enter Seller ID to add/update as Premium Seller: ")
        # Check if seller exists
        query_seller = "SELECT * FROM Seller WHERE seller_id = %s;"
        cur.execute(query_seller, (seller_id,))
        seller = cur.fetchone()
        if not seller:
            print("Seller not found.")
            input("Press Enter to continue...")
            return
        # Check if seller is already a premium seller
        query_premium = "SELECT * FROM Premium_Seller WHERE seller_id = %s;"
        cur.execute(query_premium, (seller_id,))
        premium = cur.fetchone()
        if premium:
            print("Current Premium Seller Details:")
            for key, value in premium.items():
                print(f"{key}: {value}")
            # Update the premium seller
            tier = input(f"Tier [{premium['tier']}]: ") or premium['tier']
            commission_rate = input(f"Commission Rate [{premium['commission_rate']}]: ") or premium['commission_rate']
            query_update = """
            UPDATE Premium_Seller
            SET tier = %s, commission_rate = %s
            WHERE seller_id = %s;
            """
            cur.execute(query_update, (tier, commission_rate, seller_id))
            con.commit()
            print("Premium Seller details updated successfully.")
        else:
            # Add the seller as a premium seller
            premium_since = input("Premium Since (YYYY-MM-DD): ")
            tier = input("Tier (SILVER, GOLD, PLATINUM): ")
            commission_rate = input("Commission Rate (between 0.01 and 0.10): ")
            query_insert = """
            INSERT INTO Premium_Seller (seller_id, premium_since, tier, commission_rate)
            VALUES (%s, %s, %s, %s);
            """
            cur.execute(query_insert, (seller_id, premium_since, tier, commission_rate))
            con.commit()
            print("Seller added as Premium Seller successfully.")
        input("Press Enter to continue...")
    except Exception as e:
        con.rollback()
        print("Failed to add/update Premium Seller.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def update_discount_codes():
    """
    Update discount codes.
    """
    try:
        code = input("Enter Discount Code to update: ")
        # Fetch current details
        query_code = "SELECT * FROM Discount_Code WHERE code = %s;"
        cur.execute(query_code, (code,))
        discount = cur.fetchone()
        if not discount:
            print("Discount code not found.")
            input("Press Enter to continue...")
            return
        print("Current Details:")
        for key, value in discount.items():
            print(f"{key}: {value}")
        # Get new details
        print("Enter new details (leave blank to keep current value):")
        type = input(f"Type [{discount['type']}]: ") or discount['type']
        value = input(f"Value [{discount['value']}]: ") or discount['value']
        expiry = input(f"Expiry [{discount['expiry']}]: ") or discount['expiry']
        # Update the discount code
        query_update = """
        UPDATE Discount_Code
        SET type = %s, value = %s, expiry = %s
        WHERE code = %s;
        """
        cur.execute(query_update, (type, value, expiry, code))
        con.commit()
        print("Discount code updated successfully.")
        input("Press Enter to continue...")
    except Exception as e:
        con.rollback()
        print("Failed to update discount code.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def update_promotions():
    """
    Update details of a promotion.
    """
    try:
        promotion_id = input("Enter Promotion ID to update: ")
        # Fetch current details
        query_promotion = "SELECT * FROM Promotion WHERE promotion_id = %s;"
        cur.execute(query_promotion, (promotion_id,))
        promotion = cur.fetchone()
        if not promotion:
            print("Promotion not found.")
            input("Press Enter to continue...")
            return
        print("Current Promotion Details:")
        for key, value in promotion.items():
            print(f"{key}: {value}")
        # Get new details
        print("Enter new details (leave blank to keep current value):")
        description = input(f"Description [{promotion['description']}]: ") or promotion['description']
        start_date = input(f"Start Date [{promotion['start_date']}]: ") or promotion['start_date']
        end_date = input(f"End Date [{promotion['end_date']}]: ") or promotion['end_date']
        # Update the promotion
        query_update = """
        UPDATE Promotion
        SET description = %s, start_date = %s, end_date = %s
        WHERE promotion_id = %s;
        """
        cur.execute(query_update, (description, start_date, end_date, promotion_id))
        con.commit()
        print("Promotion updated successfully.")
        input("Press Enter to continue...")
    except Exception as e:
        con.rollback()
        print("Failed to update promotion.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


def view_sales_statistics():
    """
    View total sales volume by category on the website.
    """
    try:
        query_stats = """
        SELECT c.name AS category_name, SUM(oi.quantity * oi.unit_price) AS total_sales
        FROM Order_Item oi
        JOIN Product p ON oi.product_id = p.product_id
        JOIN Category c ON p.category_id = c.category_id
        GROUP BY c.category_id;
        """
        cur.execute(query_stats)
        stats = cur.fetchall()
        if not stats:
            print("No sales data available.")
            input("Press Enter to continue...")
            return
        print("Total Sales Volume by Category:")
        for stat in stats:
            print(f"Category: {stat['category_name']}, Total Sales: {stat['total_sales']}")
        input("Press Enter to continue...")
    except Exception as e:
        print("Failed to retrieve sales statistics.")
        print(">>>>>>>>>>>>>", e)
        input("Press Enter to continue...")


# Start the program
if __name__ == "__main__":
    try:
        username = "username"
        password = "password"
        db = "Online_Marketplace_Management"

        con = pymysql.connect(
            host='localhost',
            port=3306,
            user=username,
            password=password,
            db=db,
            cursorclass=pymysql.cursors.DictCursor
        )

        if con.open:
            print("Connected to the database.")

        with con.cursor() as cur:
            main_menu()

    except Exception as e:
        print("Error:", e)
        print("Connection failed. Please check your credentials or database setup.")
        sys.exit()
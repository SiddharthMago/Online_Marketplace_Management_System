### TO RUN

Update the main code with your username and password -
```c
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
```

Download the database using the Dump.sql -
```c
mysql -u username -p Online_Marketplace_Management < Dump.sql
```

Run the program - 
```c
python3 boilerPlate.py
```
##

### COMMANDS

#### Seller Commands:
1. ADD or UPDATE a product for a particular seller - if entry with seller provided product_id and SKU exists then instead of adding we update that entry. Else we simply add a new product tuple.

    ```c
    INSERT INTO Product (product_id, SKU, name, price, stock, seller_id, category_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    name = %s, price = %s, stock = %s, category_id = %s;
    ```

2. DELETE product for a particular seller - 

    ```c
    DELETE FROM Product WHERE product_id = %s AND SKU = %s AND seller_id = %s;
    ```

3. VIEW all products of a particular seller and VIEW product_reviews for products of a particular seller -

    ```c
    SELECT product_id, name FROM Product WHERE seller_id = %s;

    SELECT pr.review_id, pr.customer_id, pr.rating, pr.comment, pr.review_date
    FROM Product_Review pr
    WHERE pr.product_id = %s;
    ```

    Commands that were not run but have been implemented -

    4. Add Product Image
    5. Delete Product Image
    6. Add Promotion
    7. Delete Promotion

#### Customer Commands:
1. VIEW all products -

    ```c
    SELECT * FROM Product;
    ```

2. VIEW product review for a particular product -

    ```c
    SELECT pr.review_id, pr.customer_id, pr.rating, pr.comment, pr.review_date
    FROM Product_Review pr
    WHERE pr.product_id = %s;
    ```

3. VIEW all customer orders -

    ```c
    SELECT o.order_id, o.transaction_id, o.rating, o.order_date, o.order_status
    FROM Orders o
    WHERE o.ordered_by = %s;
    ```   

    Commands that were not run but have been implemented -

    4. View Seller Details
    5. View Product Images
    6. View Promotions

#### Manager Commands:
1. UPDATE customer details -

    ```c
    UPDATE Customer
    SET name = %s, email = %s, street = %s, city = %s, state = %s, zip = %s
    WHERE customer_id = %s;
    ```

2. UPDATE seller details -

    ```c
    UPDATE Seller
    SET name = %s, street = %s, city = %s, state = %s, zip = %s, rating = %s
    WHERE seller_id = %s;
    ```

3. ADD or UPDATE premium seller details - if entry with provided seller_id exists then instead of adding we update that entry. Else we simply add a new premium seller tuple.

    ```c
    INSERT INTO Premium_Seller (seller_id, premium_since, tier, commission_rate)
    VALUES (%s, %s, %s, %s);

    UPDATE Premium_Seller
    SET tier = %s, commission_rate = %s
    WHERE seller_id = %s;
    ```

4. VIEW sales statistics - Product sales by volume per category.

    ```c
    SELECT c.name AS category_name, SUM(oi.quantity * oi.unit_price) AS total_sales
    FROM Order_Item oi
    JOIN Product p ON oi.product_id = p.product_id
    JOIN Category c ON p.category_id = c.category_id
    GROUP BY c.category_id;
    ```

5. UPDATE promotions - Wasnt available in video, have added a function for that.

    ```c
    UPDATE Promotion
    SET description = %s, start_date = %s, end_date = %s
    WHERE promotion_id = %s;
    ```

6. UPDATE discount codes -

    ```c
    UPDATE Discount_Code
    SET type = %s, value = %s, expiry = %s
    WHERE code = %s;
    ```

##

### ERROR HANDLING

1. Check for valid Customer, Seller and Manager IDs before further execution.

2. Check if any query is invalid before printing output and informing user accordingly.

3. Checks and handles for sellers updating/viewing data of other sellers.

4. Customer can only see necessary seller information.

5. Program doesnt quit unexpectedly while execution.

6. Error handling for initial pymysql connection setup.
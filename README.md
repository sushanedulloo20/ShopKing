# ShopKing 👑

ShopKing is a Python-based online shopping application that enables seamless interactions between administrators, customers, and delivery partners. Utilizing a MySQL database, ShopKing efficiently manages product information, customer orders, and delivery logistics through a command-line interface.

# Features

- **Admin Functionality**: Manage products, orders, and suppliers.
- **Customer Functionality**: Browse products, add items to cart, and place orders.
- **Delivery Partner Functionality**: View and manage delivery orders.

# Getting Started

To run the ShopKing application, follow these steps:

## 1. Clone the Repository:
   ```bash
   git clone https://github.com/yourusername/shopking.git](https://github.com/sushanedulloo20/ShopKing.git
   cd shopking
   ```
## 2. Install Dependencies:

Ensure you have Python installed, then install necessary packages:

a) Python version: ```3.10.12```

b) MySQL Workbench: `8.0.38`


## 3. Set Up MySQL Database:

Configure the MySQL database according to the provided schema. Update your database connection settings in the application as necessary.

## 4. Run the Application:

Start the application by executing the main Python script:
```bash
python CLI_User_Interface.py
```

## 5. Login Options:

When prompted, enter:

 `1` to log in as an admin.
 

`2` to log in as a customer.

`3` to log in as a delivery partner.

`4` to exit the application.

## 6.Admin Options:

If you logged in as an admin, you will be prompted to choose from several options. Enter the number of the option you want to select:

1. Search Products
2. Add products in stock (update quantity)
3. Update products in stock (modify existing products or add new ones)
4. Delete products (remove products from the database)
5. Search Orders (view orders)
6. Search Delivery Partners (check delivery partners and their delivery areas)
7. Search Suppliers (view suppliers)
8. OLAPs (Online Analytical Processing)

## 7. Customer Options:

If you logged in as a customer, you will also be prompted to choose from several options. Enter the number of the option you want to select:

1. Search Products (view available products)
2. Add products to Cart (add items to your shopping cart)
3. Show Cart (view your current cart)
4. Place Order (complete your purchase)
5. Show Orders (view your past orders)

## 8. Delivery Partner Options

If you logged in as a delivery partner, you will also be prompted to choose from several options. Enter the number of the option you want to select:

1. Show Orders (view available or taken orders)
2. Select Order (choose an order to deliver)
3. Exit (log out of the delivery partner interface)







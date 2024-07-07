import pprint as p
from tabulate import tabulate as tab
from datetime import date
import time
import mysql.connector as mysql
import random as r


# Connecting mysql connector
db = mysql.connect(host="localhost", user="root", password="sushane",port=3306)

mc = db.cursor(buffered=True)
mc.execute("USE KKT_SHOPKING;")

# Admin function used for showing OLAP queries


def olap(aid):
    q = int(
        input(
            """
    1)  Showing number of customers in cities and states
    2)  Showing all delivery partners with rating and number of orders 
    3)  showing number of orders in months and year
    4)  Showing number of customers in each state\n
"""
        )
    )
    if q == 1:
        mc.execute(
            """ 
SELECT state, city, count(customer_ID) AS Num_customers 
FROM customers
GROUP BY state, city with rollup;"""
        )
        data = mc.fetchall()
        print(tab(data, headers=["State", "City", "Number of customers"]))
    elif q == 2:
        mc.execute(
            """
SELECT dp.rating,dp.name,COUNT(*) as num_orders FROM handles as h INNER JOIN del_partners as dp
ON h.dp_ID = dp.dp_ID GROUP BY dp.name,dp.rating with rollup Order by dp.rating desc,dp.name;
"""
        )
        data = mc.fetchall()
        print(tab(data, headers=["Rating", "Delivery_Partner", "Number of Orders"]))
    elif q == 3:
        mc.execute(
            """SELECT YEAR(order_Date) as Year, MONTHNAME(order_Date) as Month, COUNT(*) as num_orders , SUM(orders.payment_amount)
FROM orders
GROUP BY Year, Month with rollup
Order by Year,Month """
        )
        data = mc.fetchall()
        print(tab(data, headers=["Year", "Month", "Number of Orders", "Revenue"]))
    elif q == 4:
        mc.execute(
            """ SELECT category_ID,prod_ID,sum(stock_quantity)
FROM products 
GROUP BY category_ID,prod_ID with rollup
order by category_ID; """
        )
        data = mc.fetchall()
        print(tab(data, headers=["Category_ID", "Products_ID", "Quantity"]))
    elif q == 5:
        return
    olap(aid)

ord_id = 101

def addorder(cid, aid, pay_t):
    global ord_id
    t = time.strftime("%H:%M:%S", time.localtime())
    if t[0:2] == "24":
        o = "00"
    else:
        o = str(int(t[0] + t[1]) + 1)
    # print(date.today(), t, o + t[2:8])
    mc.execute(f"SELECT total_price FROM cart WHERE cart_ID={cid}")
    data = mc.fetchall()
    amt = int(data[0][0])
    mc.execute(
        f"""Insert into orders values({ord_id},"{date.today()}","{t}","{o+t[2:8]}",
"Packing",{cid},{aid},{amt},"{pay_t}",NULL)"""
    )
    mc.execute(f"DELETE FROM contain where cart_ID={cid}")
    mc.execute(f"update cart set total_price=0 where customer_ID={cid}")
    ord_id += 1
    # db.commit()
    print("    Order Accepted")

def Admin(aid):
    q = int(
        input(
            """
1) Search Products
2) Add products in stock
3) Update products in stock
4) Delete products
5) Search Orders
6) search delivery partners
7) Search Suppliers
8) OLAPs
    -->"""
        )
    )

    if q==1:
        searchproducts()
    elif q == 2:
        name = input("  Enter Name         :")
        desc = input("  Enter decscription :")
        price = input("  Enter Price        :")
        stk_qty = int(input("  Enter quantity     :"))
        cat_ID=int(input("  Enter category_ID"))
        # link=""
        try:
            mc.execute(
                f"""INSERT INTO PRODUCTS(name,description,price,stock_quantity,category_ID,link) 
        values('{name}','{desc}',{price},{stk_qty},{cat_ID},"")""")
            print("  Stock Updated succesfully")
        except Exception as e:
            print(e)
            print("   Error! Try again")
    elif q == 3:

        prod_ID = int(input("  Enter product ID   : "))
        print("  Enter updated Values")
        name = input("   Enter Name         : ")
        desc = input("   Enter decscription : ")
        price = input("   Enter Price        : ")
        stk_qty = int(input("   Enter quantity     : "))
        cat_ID = int(input("   Enter Category_ID  : "))
        # link=""
        try :
            mc.execute(
            f"""
            UPDATE PRODUCTS 
            SET name='{name}',description='{desc}',price={price},stock_quantity={stk_qty},category_ID={cat_ID}
            WHERE prod_ID={prod_ID}"""
            )
            print("   Stock updated successfully!")
        except:
            print("   Error! Try Again")
    elif q == 4:
        prod_ID = int(input("   Enter product ID  : "))
        mc.execute(f"""DELETE FROM PRODUCTS WHERE prod_ID={prod_ID}""")
        print("   Stock Updated successfully")
    elif q == 5: 
        s = int(
            input(
                """
  Search by 
    1) Show All
    2) Status
    3) Order_Amount
    4) Customer ID
    5) Time
    --> """
            )
        )
        if s==1:
            mc.execute(
                f"""
SELECT o.order_ID,o.order_Date,o.order_Time ,o.delivery_time,o.Status,o.payment_amount,d.name as Del_parnter,s.name as supplier
from orders as o 
inner join handles as h on o.order_ID = h.order_ID
inner join customers as c on c.customer_ID=o.customer_ID
inner join pack as p on h.order_ID=p.order_ID
inner join supplier as s on s.supp_ID=p.supp_ID
inner join del_partners as d on d.dp_ID=h.dp_ID 
order by o.order_Date,o.order_time"""
            )
            data = mc.fetchall()
            print(
                    tab(
                        data,
                        headers=[
                        "Order_ID",
                        "Order_Date",
                        "Order_Time",
                        "Delivery_Time",
                        "Status",
                        "payment_amount",
                        "Delivery Partner",
                        "Supplier"
                        ],
                    )
                )
        elif s == 2:
            status = int(
                input(
                    """
      1) Delivered 
      2) On the Way
      3) Packing"""
                )
            )
            if status == 1:

                mc.execute(
            f"""SELECT o.order_ID,o.order_Date,o.order_Time ,o.delivery_time,o.Status,o.payment_amount,d.name as Del_parnter,s.name as supplier
from orders as o 
inner join handles as h on o.order_ID = h.order_ID
inner join customers as c on c.customer_ID=o.customer_ID
inner join pack as p on h.order_ID=p.order_ID
inner join supplier as s on s.supp_ID=p.supp_ID
inner join del_partners as d on d.dp_ID=h.dp_ID
Where Status = 'Delivered'"""
        )
                data = mc.fetchall()
                print(
                    tab(
                        data,
                        headers=[
                        "Order_ID",
                        "Order_Date",
                        "Order_Time",
                        "Delivery_Time",
                        "Status",
                        "payment_amount",
                        "Delivery Partner",
                        "Supplier"
                        ],
                    )
                )
            elif status == 2:
                mc.execute(f"""
SELECT o.order_ID,o.order_Date,o.order_Time ,o.delivery_time,o.Status,o.payment_amount,d.name as Del_parnter,s.name as supplier
from orders as o 
inner join handles as h on o.order_ID = h.order_ID
inner join customers as c on c.customer_ID=o.customer_ID
inner join pack as p on h.order_ID=p.order_ID
inner join supplier as s on s.supp_ID=p.supp_ID
inner join del_partners as d on d.dp_ID=h.dp_ID
where STATUS='Ontheway'""")
                data = mc.fetchall()
                print(
                    tab(
                        data,
                        headers=[
                        "Order_ID",
                        "Order_Date",
                        "Order_Time",
                        "Delivery_Time",
                        "Status",
                        "payment_amount",
                        "Delivery Partner",
                        "Supplier"
                        ],
                    )
                )
            elif status == 3:
                mc.execute(f"""
SELECT o.order_ID,o.order_Date,o.order_Time ,o.delivery_time,o.Status,o.payment_amount,d.name as Del_parnter,s.name as supplier
from orders as o 
inner join handles as h on o.order_ID = h.order_ID
inner join customers as c on c.customer_ID=o.customer_ID
inner join pack as p on h.order_ID=p.order_ID
inner join supplier as s on s.supp_ID=p.supp_ID
inner join del_partners as d on d.dp_ID=h.dp_ID
where STATUS='Packing'""")
                
                data = mc.fetchall()
                print(
                    tab(
                        data,
                        headers=[
                        "Order_ID",
                        "Order_Date",
                        "Order_Time",
                        "Delivery_Time",
                        "Status",
                        "payment_amount",
                        "Delivery Partner",
                        "Supplier"
                        ],
                    )
                )
        elif s == 3:
            low_lim = int(input("Enter lower limit"))
            high_lim = int(input("Enter Higher limit"))
            mc.execute(
                f"""
SELECT o.order_ID,o.order_Date,o.order_Time ,o.delivery_time,o.Status,o.payment_amount,d.name as Del_parnter,s.name as supplier
from orders as o 
inner join handles as h on o.order_ID = h.order_ID
inner join customers as c on c.customer_ID=o.customer_ID
inner join pack as p on h.order_ID=p.order_ID
inner join supplier as s on s.supp_ID=p.supp_ID
inner join del_partners as d on d.dp_ID=h.dp_ID 
where {low_lim}<=payment_amount AND payment_amount<={high_lim}"""
            )
            data = mc.fetchall()
            print(
                    tab(
                        data,
                        headers=[
                        "Order_ID",
                        "Order_Date",
                        "Order_Time",
                        "Delivery_Time",
                        "Status",
                        "payment_amount",
                        "Delivery Partner",
                        "Supplier"
                        ],
                    )
                )
        elif s == 4:
            cus = int(input("      Enter Customer ID : "))
            mc.execute(f"""
SELECT o.order_ID,o.order_Date,o.order_Time ,o.delivery_time,o.Status,o.payment_amount,d.name as Del_parnter,s.name as supplier
from orders as o 
inner join handles as h on o.order_ID = h.order_ID
inner join customers as c on c.customer_ID=o.customer_ID
inner join pack as p on h.order_ID=p.order_ID
inner join supplier as s on s.supp_ID=p.supp_ID
inner join del_partners as d on d.dp_ID=h.dp_ID 
 where o.CUSTOMER_ID={cus}""")
            data = mc.fetchall()
            print(
                    tab(
                        data,
                        headers=[
                        "Order_ID",
                        "Order_Date",
                        "Order_Time",
                        "Delivery_Time",
                        "Status",
                        "payment_amount",
                        "Delivery Partner",
                        "Supplier"
                        ],
                    )
                )
        elif s == 5:
            low_lim = (input("      Enter Start Date (YYYY-MM-DD)"))
            high_lim = (input("      Enter End date (YYYY-MM-DD)"))
            mc.execute(
                f"""
SELECT o.order_ID,o.order_Date,o.order_Time ,o.delivery_time,o.Status,o.payment_amount,d.name as Del_parnter,s.name as supplier
from orders as o 
inner join handles as h on o.order_ID = h.order_ID
inner join customers as c on c.customer_ID=o.customer_ID
inner join pack as p on h.order_ID=p.order_ID
inner join supplier as s on s.supp_ID=p.supp_ID
inner join del_partners as d on d.dp_ID=h.dp_ID 
where '{low_lim}'<=order_Date AND order_Date<='{high_lim}'"""
            )
            data = mc.fetchall()
            print(
                    tab(
                        data,
                        headers=[
                        "Order_ID",
                        "Order_Date",
                        "Order_Time",
                        "Delivery_Time",
                        "Status",
                        "payment_amount",
                        "Delivery Partner",
                        "Supplier"
                        ],
                    )
                )
    elif q == 6:
        s = int(
            input(
                """
  Search by 
    1) Show all
    2) name
    3) ID 
    4) rating
    --> """
            )
        )
        if s==1:
            s2=int(input("""
      Sort By 
        1) Name A to Z
        2) Rating High to Low
        3) Rating Low to High
        --> """))
            if s2==1:
                mc.execute(f"SELECT dp_ID,name,rating from del_partners ORDER BY name")
                data = mc.fetchall()
                print(tab(data,headers=["ID","name","rating"]))
            elif s2==2:
                mc.execute(f"SELECT dp_ID,name,rating from del_partners ORDER BY rating desc")
                data = mc.fetchall()
                print(tab(data,headers=["ID","name","rating"]))
            elif s2==3:
                mc.execute(f"SELECT dp_ID,name,rating from del_partners ORDER BY rating")
                data = mc.fetchall()
                print(tab(data,headers=["ID","name","rating"]))
        elif s == 2:
            name = input("      Enter name")
            mc.execute(f"SELECT dp_ID,name,rating from del_partners where name like '{name}%'")
            data = mc.fetchall()
            print(
                tab(
                    data,
                    headers=[
                    "ID",
                    "name",
                    "rating",
                    ],
                )
            )
        elif s == 3:
            id = input("      Enter ID")
            mc.execute(f"SELECT dp_ID,name,rating from del_partners where dp_ID={id}")
            data = mc.fetchall()
            print(
                tab(
                    data,
                    headers=[
                    "ID",
                    "name",
                    "rating",
                    ],
                )
            )
        elif s == 4:
            rating = input("      Enter rating")
            mc.execute(f"SELECT dp_ID,name,rating from del_partners where rating={rating}")
            data = mc.fetchall()
            print(
                tab(
                    data,
                    headers=[
                    "ID",
                    "name",
                    "rating",
                    ],
                )
            )
    elif q == 7:
        s = int(
            input(
                """
  Search by
    1) ID 
    2) name
    3) pincode
    4) phone
    --> """
            )
        )
        if s == 1:
            id = input("      Enter ID : ")
            mc.execute(f"SELECT supp_ID,name,sector,city,state,pincode,phone from supplier where supp_ID={id}")
            data=mc.fetchall()
            print(tab(data,headers=["ID","Name","Sector","City","State","Pincode","Phone"]))
        elif s == 2:
            name = input("      Enter name : ")
            mc.execute(f"SELECT * from supplier where name like '{name}%'")
            data=mc.fetchall()
            print(tab(data,headers=["ID","Name","Sector","City","State","Pincode","Phone"]))
        
        elif s == 3:
            pinc = int(input("      Enter Pincode : "))
            mc.execute(f"SELECT * from supplier where pincode like '{pinc}%'")
            data=mc.fetchall()
            print(tab(data,headers=["ID","Name","Sector","City","State","Pincode","Phone"]))
        
        elif s == 4:
            phone = input("      Enter phone number : ")
            mc.execute(f"SELECT * from supplier where phone like '{phone}%'")
            data=mc.fetchall()
            print(tab(data,headers=["ID","Name","Sector","City","State","Pincode","Phone"]))
    elif q == 8:
        olap(aid)
    elif q==9:
        return
    Admin(aid)

def searchproducts():
    q = int(
        input(
            """
  1) Show All Product
  2) by name
  3) Category
  4) exit
  --> """
        )
    )
    if q == 1:
        mc.execute(f"SELECT * FROM PRODUCTS")
        q1 = int(
            input(
                """
    Sort By
      1) Name A to Z
      2) Price High to Low
      3) Price Low to High
      Enter to Exit
      --> """
            )
        )
        if q1 == 1:
            mc.execute(f"SELECT prod_ID,name,description,price,stock_quantity FROM PRODUCTS ORDER BY NAME")
            data = mc.fetchall()
            print(tab(data,headers=["ID","Name","Description","Price","stock_quantity"])
        )
        elif q1 == 2:
            mc.execute(f"SELECT prod_ID,name,description,price,stock_quantity FROM PRODUCTS ORDER BY PRICE DESC")
            data = mc.fetchall()
            print(tab(data,headers=["ID","Name","Description","Price","stock_quantity"]))
        elif q1 == 3:
            mc.execute(f"SELECT prod_ID,name,description,price,stock_quantity FROM PRODUCTS ORDER BY PRICE")
            data = mc.fetchall()
            print(tab(data,headers=["ID","Name","Description","Price","stock_quantity"]))
    elif q == 2:
        name = input("Enter Name : ")
        mc.execute(f"SELECT prod_ID,name,description,price,stock_quantity FROM PRODUCTS WHERE NAME LIKE '{name}%'")
        data = mc.fetchall()
        print(tab(data,headers=["ID","Name","Description","Price","stock_quantity"]))
    elif q == 3:
        id = int(input("""
    Enter category ID
      1) Vegetables & Fruits
      2) Dairy
      3) Beverages
      4) Snacks
      5) Bakery
      6) Sweets
      7) Non-Veg
      8) Personal care
      10) Daily Use 
      --> """))
        mc.execute(f"SELECT prod_ID,name,description,price,stock_quantity FROM PRODUCTS WHERE category_ID={id}")
        data = mc.fetchall()
        print(tab(data,headers=["ID","Name","Description","Price","stock_quantity"],))
    elif q==4:
        return
    searchproducts()

def Customer(cid):
    q = int(
        input(
            """
1) Search Products
2) Add products to Cart
3) Show Cart
4) place order
5) Show Orders
6) Exit
"""
        )
    )
    if q==1:
        searchproducts()
    elif q == 2:
        b = int(input("  Enter products ID : "))
        qty = int(input("  Enter Quantity : "))
        mc.execute(f"Select stock_quantity from products where prod_ID={b}")
        data=mc.fetchall()
        if(data[0][0] >= qty):
            mc.execute(f"Insert Into contain values({cid},{b},{qty})")
            print("   Product Added Successfully")
        elif(data[0][0]==[]):
            print("   Product not available")
        else:
            print("Only ",data[0][0]," are left!")
    elif q == 3:
        mc.execute(
            f"""SELECT p.prod_ID, p.name,p.description,p.price,c.quantity,
(p.price*c.quantity) total_price FROM contain c JOIN products 
p on p.prod_ID = c.prod_ID WHERE c.cart_ID = '{cid}'"""
        )
        data = mc.fetchall()
        print(tab(data,headers=["Prod_ID","Name","Description","Price","Quantity","Total Price",],))
        mc.execute(f"SELECT total_price FROM cart WHERE cart_ID={cid}")
        data = mc.fetchall()
        print("\n  TOTAL AMOUNT = ₹", data[0][0])
    elif q == 4:
        pay_t = input("Enter to pay")
        pay_t = time.strftime("%H:%M:%S", time.localtime())
        addorder(cid, r.randint(1, 101), pay_t)
    elif q == 5:
        mc.execute(
            f"""SELECT o.order_ID,o.order_Date,o.order_Time ,o.delivery_time,o.Status,o.payment_amount,h.dp_ID,p.supp_ID 
from orders as o inner join handles as h 
on o.order_ID = h.order_ID 
inner join pack as p on h.order_ID=p.order_ID 
WHERE o.customer_ID = {cid}"""
        )
        data = mc.fetchall()
        print(tab(data,headers=["order_ID","Date","Time","Delivery_Time","Status","payment_amount","dp_ID","Supp_ID",],))
    elif q == 6:
        return
    Customer(cid)

def del_par(did):
    q=int(input("""
    1) Show orders
    2) Select Order
    3) Exit
    --> """))
    if q==1:
        mc.execute(
            f"""
SELECT o.order_ID,o.order_Date,o.order_Time ,o.delivery_time,o.Status,o.payment_amount,d.name as Del_parnter,s.name as supplier
from orders as o 
inner join handles as h on o.order_ID = h.order_ID
inner join customers as c on c.customer_ID=o.customer_ID
inner join pack as p on h.order_ID=p.order_ID
inner join supplier as s on s.supp_ID=p.supp_ID
inner join del_partners as d on d.dp_ID=h.dp_ID 
WHERE h.dp_ID={did} ORDER BY o.status"""
            )
        data = mc.fetchall()
        print(tab(data,headers=["Order_ID","Order_Date","Order_Time","Delivery_Time","Status","payment_amount","Delivery Partner","Supplier"]))
    elif q==2:
        s=int(input("      Enter order id : "))
        mc.execute(
            f"""
SELECT o.order_ID,o.Status,o.payment_amount,c.name,c.sector,c.city,c.state,c.pincode,s.name
from orders as o 
inner join handles as h on o.order_ID = h.order_ID
inner join customers as c on c.customer_ID=o.customer_ID
inner join pack as p on h.order_ID=p.order_ID
inner join supplier as s on s.supp_ID=p.supp_ID
inner join del_partners as d on d.dp_ID=h.dp_ID 
WHERE h.dp_ID={did} And o.order_ID={s}""")
        data = mc.fetchall()
        print(tab(data,headers=["Order_ID","Status","Amount","Name","Sector","City","State","Pincode","Supplier"]))
        if(data[0][1]=="Packing"):
            u=(input("""
        1) Picked up
        Enter to exit"""))
            if(u=='1'):
                mc.execute(f"""
UPDATE orders 
SET status='ontheway'
Where order_ID={s}""")
                print("      Status Update to On the way")    
        elif (data[0][1]=="ontheway"):
            u=(input("""
            1) Delivered
            Enter to exit"""))
            if(u=='1'):
                t = time.strftime("%H:%M:%S", time.localtime())
                if t[0:2] == "24":
                    o = "00"
                else:
                    o = str(int(t[0] + t[1]) + 1)
                mc.execute(f"""
UPDATE orders 
SET status='Delivered',
delivery_Time='{t}'
Where order_ID={s}""")
                print("      Status Update to Delivered")    
    elif q==3:
        return
    del_par(did)

# Id and passwords
# Admin --> '1', 'JBH18USU8MX'
# Customer --> '1'	'NHY46ICL5SB'
# del_partner -> 28 -> LEG50ZWU5UV
def Login():
    user = int(input("""
1) for admin 
2) for Customer
3) Delivery Partner
4) exit
--> """))
    if user == 1:
        aid = int(input("Enter Admin ID : "))
        pwd = input("Enter Password : ")
        mc.execute(f"SELECT password from admins where admin_id={aid}")
        data=mc.fetchall()
        if(data[0][0]==pwd):
            print("Logged in Successfully")
            Admin(aid)
        else:
            print("Wrong Password ! Try Again !")                    
    elif user == 2:
        cid = (input("Enter customer ID : "))
        pwd = input("Enter Password : ")
        mc.execute(f"SELECT password from customers where customer_ID={cid}")
        data=mc.fetchall()
        if(data[0][0]==pwd):
            print("Logged in Successfully")
            Customer(cid)
        else:
            print("Wrong Password ! Try Again !")  
    elif user == 3:
        cid = int(input("Enter Delivery Partner ID : "))
        pwd = input("Enter Password : ")
        mc.execute(f"SELECT password from del_partners where dp_ID={cid} ")
        data=mc.fetchall()
        if(data[0][0]==pwd):
            print("Logged in Successfully")
            del_par(cid)
        else:
            print("Wrong Password ! Try Again !")  
    elif user == 4:
        return 
    Login()

Login()
mc.close()

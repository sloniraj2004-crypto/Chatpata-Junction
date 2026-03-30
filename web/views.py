import MySQLdb
import os
import pymysql
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.contrib import messages
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def fd(request):
    return render(request, 'fd.html')

def nontype(request):
    return render(request, 'non-veg.html')

def adven(request):
    return render(request, 'vegetables.html')

def dare(request):
    return render(request, 'regional.html')

def humble(request):
    return render(request, 'fruit.html')

def care(request):
    return render(request, 'spicy.html')

def topa(request):
    return render(request, 'sweet.html')

def hero(request):
    return render(request, 'sour.html')

def pagal(request):
    return render(request, 'sweet & sour.html')

def bby(request):
    return render(request, 'oil.html')

def each(request):
    return render(request, 'vinegar.html')

def pen(request):
    return render(request, 'sun.html')

def scale(request):
    return render(request, 'offers.html')

def book(request):
    return render(request, 'about_us.html')

def comb(request):
    return render(request, 'contact.html')

def now(request):
    return render(request, 'shop.html')

def phn(request):
    return render(request, 'FAQs.html')

def paper(request):
    return render(request, 'shipping.html')

def dell(request):
    return render(request, 'return.html')

def hp(request):
    return render(request, 'privacy.html')

def sec(request):
    return render(request, 'header.html')

def boat(request):
    return render(request, 'footer.html')

def sidebar(request):
    return render(request, 'sidebar.html')

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        print("NAME =", name)
        print("EMAIL =", email)
        print("PASSWORD =", password)
        print("ADDRESS =", address)
        print("PHONE =", phone)

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customers WHERE Email=%s", [email])
                existing_user = cursor.fetchone()

                if existing_user:
                    messages.error(request, "Email already registered.")
                    return render(request, "register.html")

                cursor.execute("""
                    INSERT INTO customers (Name, Email, Password, Address, Phone_Number)
                    VALUES (%s, %s, %s, %s, %s)
                """, [name, email, password, address, phone])

            messages.success(request, "Registration successful. Please login.")
            return redirect("bow")

        except Exception as e:
            messages.error(request, f"Database Error: {e}")
            return render(request, "register.html")

    return render(request, "register.html")

#......login........#
'''
def bow(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Customer_ID, Name, Email
                FROM customers
                WHERE Email=%s AND Password=%s
            """, [email, password])
            user = cursor.fetchone()

        if user:
            request.session['user_id'] = user[0]
            request.session['user_name'] = user[1]
            request.session['user_email'] = user[2]
            request.session['login_success'] = True
            return redirect('profile')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "login page.html")

def profile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('bow')   # login page

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()
        profile_image = request.FILES.get('profile_image')

        with connection.cursor() as cursor:
            if profile_image:
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'profile_images')
                os.makedirs(upload_dir, exist_ok=True)

                fs = FileSystemStorage(location=upload_dir)
                filename = fs.save(profile_image.name, profile_image)
                image_name = 'profile_images/' + filename

                cursor.execute("""
                    UPDATE customers
                    SET Name=%s, Email=%s, Address=%s, Phone_Number=%s, Profile_Image=%s
                    WHERE Customer_ID=%s
                """, [name, email, address, phone, image_name, user_id])
            else:
                cursor.execute("""
                    UPDATE customers
                    SET Name=%s, Email=%s, Address=%s, Phone_Number=%s
                    WHERE Customer_ID=%s
                """, [name, email, address, phone, user_id])

        request.session['user_name'] = name
        return redirect('/profile/?updated=1')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Customer_ID, Name, Email, Address, Phone_Number, Profile_Image
            FROM customers
            WHERE Customer_ID=%s
        """, [user_id])
        row = cursor.fetchone()

    if not row:
        return redirect('bow')

    user = {
        'Customer_ID': row[0],
        'Name': row[1],
        'Email': row[2],
        'Address': row[3],
        'Phone_Number': row[4],
        'Profile_Image': row[5],
    }

    updated = request.GET.get('updated')
    login_success = request.session.pop('login_success', False)


    return render(request, 'profile.html', {
        'user': user,
        'updated': updated,
        'login_success': login_success
    })

#....user dashboard....#
def dashboard(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    with connection.cursor() as cursor:
        # customer profile
        cursor.execute("""
            SELECT Customer_ID, Name, Email, Address, Phone_Number, Profile_Image
            FROM customers
            WHERE Customer_ID = %s
        """, [user_id])
        customer = cursor.fetchone()

        # total orders
        cursor.execute("""
            SELECT COUNT(*)
            FROM order_db
            WHERE Customer_ID = %s
        """, [user_id])
        total_orders = cursor.fetchone()[0] or 0

        # total spent from paid payments
        cursor.execute("""
            SELECT COALESCE(SUM(p.Amount), 0)
            FROM payment_db p
            INNER JOIN order_db o ON p.Order_No = o.Order_No
            WHERE o.Customer_ID = %s AND p.Payment_Status = 'Paid'
        """, [user_id])
        total_spent = cursor.fetchone()[0] or 0

        # total feedbacks
        cursor.execute("""
            SELECT COUNT(*)
            FROM feedback
        """)
        total_feedbacks = cursor.fetchone()[0] or 0

        # recent orders
        cursor.execute("""
            SELECT Order_No, Amount, Order_Date, Order_Status
            FROM order_db
            WHERE Customer_ID = %s
            ORDER BY Order_No DESC
            LIMIT 5
        """, [user_id])
        recent_orders = cursor.fetchall()

    context = {
        'user_name': user_name,
        'customer': customer,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'total_feedbacks': total_feedbacks,
        'recent_orders': recent_orders,
    }

    return render(request, 'dashboard.html', context)
'''



def bow(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Customer_ID, Name, Email
                FROM customers
                WHERE Email = %s AND Password = %s
            """, [email, password])
            user = cursor.fetchone()

        if user:
            request.session['user_id'] = user[0]
            request.session['user_name'] = user[1]
            request.session['user_email'] = user[2]
            request.session['login_success'] = True

            return redirect('profile')   # ya dashboard karna ho to dashboard likh do
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "login page.html")


def profile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "Please login first.")
        return redirect('bow')

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()
        profile_image = request.FILES.get('profile_image')

        with connection.cursor() as cursor:
            if profile_image:
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'profile_images')
                os.makedirs(upload_dir, exist_ok=True)

                fs = FileSystemStorage(location=upload_dir)
                filename = fs.save(profile_image.name, profile_image)
                image_name = 'profile_images/' + filename

                cursor.execute("""
                    UPDATE customers
                    SET Name=%s, Email=%s, Address=%s, Phone_Number=%s, Profile_Image=%s
                    WHERE Customer_ID=%s
                """, [name, email, address, phone, image_name, user_id])
            else:
                cursor.execute("""
                    UPDATE customers
                    SET Name=%s, Email=%s, Address=%s, Phone_Number=%s
                    WHERE Customer_ID=%s
                """, [name, email, address, phone, user_id])

        # session update bhi kar do taaki navbar/profile me new name turant aaye
        request.session['user_name'] = name
        request.session['user_email'] = email

        return redirect('/profile/?updated=1')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Customer_ID, Name, Email, Address, Phone_Number, Profile_Image
            FROM customers
            WHERE Customer_ID = %s
        """, [user_id])
        row = cursor.fetchone()

    if not row:
        messages.error(request, "User not found.")
        return redirect('bow')

    user = {
        'Customer_ID': row[0],
        'Name': row[1],
        'Email': row[2],
        'Address': row[3],
        'Phone_Number': row[4],
        'Profile_Image': row[5],
    }

    updated = request.GET.get('updated')
    login_success = request.session.pop('login_success', False)
    user_name = request.session.get('user_name')

    return render(request, 'profile.html', {
        'user': user,
        'user_name': user_name,
        'updated': updated,
        'login_success': login_success
    })


def dashboard(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')

    if not user_id:
        messages.error(request, "Please login first.")
        return redirect('bow')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Customer_ID, Name, Email, Address, Phone_Number, Profile_Image
            FROM customers
            WHERE Customer_ID = %s
        """, [user_id])
        customer = cursor.fetchone()

        cursor.execute("""
            SELECT COUNT(*)
            FROM order_db
            WHERE Customer_ID = %s
        """, [user_id])
        total_orders = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT COALESCE(SUM(p.Amount), 0)
            FROM payment_db p
            INNER JOIN order_db o ON p.Order_No = o.Order_No
            WHERE o.Customer_ID = %s AND p.Payment_Status = 'Paid'
        """, [user_id])
        total_spent = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT COUNT(*)
            FROM feedback
        """)
        total_feedbacks = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT Order_No, Amount, Order_Date, Order_Status
            FROM order_db
            WHERE Customer_ID = %s
            ORDER BY Order_No DESC
            LIMIT 5
        """, [user_id])
        recent_orders = cursor.fetchall()

    context = {
        'user_name': user_name,
        'customer': customer,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'total_feedbacks': total_feedbacks,
        'recent_orders': recent_orders,
    }

    return render(request, 'dashboard.html', context)

'''
def logout_view(request):
    request.session.flush()
    messages.success(request, "Logout successful.")
    return redirect('bow')
    '''
#.....user order....#
def orders(request):
    orders_data = []
    total_orders = 0
    pending_orders = 0
    delivered_orders = 0
    cancelled_orders = 0

    with connection.cursor() as cursor:
        # Total orders
        cursor.execute("SELECT COUNT(*) FROM order_db")
        total_orders = cursor.fetchone()[0]

        # Pending orders
        cursor.execute("SELECT COUNT(*) FROM order_db WHERE Order_Status = 'Pending'")
        pending_orders = cursor.fetchone()[0]

        # Delivered orders
        cursor.execute("SELECT COUNT(*) FROM order_db WHERE Order_Status = 'Delivered'")
        delivered_orders = cursor.fetchone()[0]

        # Cancelled orders
        cursor.execute("SELECT COUNT(*) FROM order_db WHERE Order_Status = 'Cancelled'")
        cancelled_orders = cursor.fetchone()[0]

        # All orders
        cursor.execute("""
            SELECT Order_No, Customer_ID, Amount, Order_Date, Order_Status
            FROM order_db
            ORDER BY Order_No DESC
        """)
        rows = cursor.fetchall()

        for row in rows:
            orders_data.append({
                'Order_No': row[0],
                'Customer_ID': row[1],
                'Amount': row[2],
                'Order_Date': row[3],
                'Order_Status': row[4],
            })

    return render(request, "orders.html", {
        "orders": orders_data,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,
    })
    
    # ================= USER PLACE ORDER =================
def place_order(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    if request.method == "POST":
        amount = request.POST.get("amount")

        if not amount:
            messages.error(request, "Amount missing.")
            return redirect("checkout")

        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="chatpata",   # yahan apna database name likho
            port=3306
        )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO order_db (Customer_ID, Amount, Order_Date, Order_Status)
            VALUES (%s, %s, %s, %s)
        """, (user_id, amount, date.today(), "Placed"))

        conn.commit()
        conn.close()

        messages.success(request, "Order placed successfully.")
        return redirect("orders")

    return redirect("checkout")

#...user payment...#   
def payment(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Payment_ID, Order_No, Amount, Payment_Status
            FROM payment_db
            ORDER BY Payment_ID DESC
        """)
        payments = cursor.fetchall()
       
    return render(request, 'payment.html', {
        'payments': payments,
        'user_name': user_name
    })

#.....admin dashboard....# 
def alogin(request):
    if request.session.get('admin_id'):
        return redirect('adashboard')

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Admin_ID, Username
                FROM admin_db
                WHERE Username=%s AND Password=%s
            """, [username, password])

            admin = cursor.fetchone()

        if admin:
            request.session['admin_id'] = admin[0]
            request.session['admin_name'] = admin[1]
            request.session['admin_login_success'] = True

            return redirect('adashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'alogin.html')

def adashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM product_db")
        total_products = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM user_db")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM order_db")
        total_orders = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(amount),0) FROM order_db")
        total_revenue = cursor.fetchone()[0]

        cursor.execute("SELECT Product_ID, Product_Name, Category, Price FROM product_db ORDER BY Product_ID DESC LIMIT 5")
        recent_products = cursor.fetchall()

        cursor.execute("SELECT order_no, customer_id, amount, order_status FROM order_db ORDER BY order_no DESC LIMIT 5")
        recent_orders = cursor.fetchall()

        cursor.execute("SELECT User_ID, User_Name, User_Email, User_Number FROM user_db ORDER BY User_ID DESC LIMIT 5")
        recent_users = cursor.fetchall()

    return render(request, 'adashboard.html', {
        'total_products': total_products,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_products': recent_products,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
    })

def adashboard(request):
    return render( request,"adashboard.html")

def product(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM product_db
            ORDER BY Product_ID DESC
        """)
        products = cursor.fetchall()

    return render(request, 'product.html', )

def users(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Customer_ID, Name, Email, Phone_Number, Address, Profile_Image
            FROM customers
            ORDER BY Customer_ID DESC
        """)
        users = cursor.fetchall()

    return render(request, 'users.html', {'users': users})

def view_user(request, customer_id):
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Customer_ID, Name, Email, Phone_Number, Address, Profile_Image
            FROM customers
            WHERE Customer_ID = %s
        """, [customer_id])
        user = cursor.fetchone()

    return render(request, 'view_user.html', {'user': user})

def block_user(request, customer_id):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM customers WHERE Customer_ID = %s", [customer_id])
        messages.success(request, "User removed successfully.")
    return redirect('users')

def aorders(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Order_No, Customer_ID, Amount, Order_Date, Order_Status
            FROM order_db
            ORDER BY Order_No DESC
        """)
        orders = cursor.fetchall()

    return render(request, 'aorders.html', {'orders': orders})

def place_order(request):
    if request.method == 'POST':
        customer_id = request.session.get('user_id')
        amount = request.POST.get('amount')   # ya cart total se lo
        order_date = date.today()
        order_status = 'Placed'

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO order_db (Customer_ID, Amount, Order_Date, Order_Status)
                VALUES (%s, %s, %s, %s)
            """, [customer_id, amount, order_date, order_status])
        return redirect('order_success')

def apayment(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Payment_ID, Order_No, Amount, Payment_Status
            FROM payment_db
            ORDER BY Payment_ID DESC
        """)
        payments = cursor.fetchall()
    return render(request, 'apayment.html', {'payments': payments})


def logout(request):
    request.session.flush()
    return redirect('home')

#......checkout....#
def kok(request):
    cart = request.session.get("cart", [])
    subtotal = sum(item["price"] * item["qty"] for item in cart)
    delivery_charge = 40 if subtotal > 0 else 0
    discount = 0
    total = subtotal + delivery_charge - discount

    if request.method == "POST":
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect("kok")

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        pincode = request.POST.get("pincode")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        payment_method = request.POST.get("payment_method")
        amount = request.POST.get("amount")
        request.session["cart"] = []
        request.session.modified = True

        messages.success(request, "Order placed successfully!")
        return redirect("order_success")

        if customer_id:
            messages.success(request, "Order placed successfully!")
            return render('ad_feedback')
    return render(request, "checkout.html", {
        "cart_items": cart,
        "subtotal": subtotal,
        "delivery_charge": delivery_charge,
        "discount": discount,
        "total": total,
    })

def ad_feedback(request):
    if request.method == "POST":
        feedback_text = request.POST.get("feedback")
        rating = request.POST.get("rating")

        if not feedback_text or not rating:
            messages.error(request, "Something went wrong, please try again!")
            return redirect('ad_feedback')

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO feedback (Feedback, Rating)
                    VALUES (%s, %s)
                """, [feedback_text, rating])

            messages.success(request, "Thanks! We appreciate your input 😊✨")
            return redirect('ad_feedback')

        except Exception as e:
            print("FEEDBACK INSERT ERROR =", e)
            messages.error(request, "Something went wrong, please try again!")
            return redirect('ad_feedback')

    return render(request, "ad_feedback.html")


#......cart.....#
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        price = int(data.get("price"))

        cart = request.session.get("cart", [])

        found = False
        for item in cart:
            if item["name"] == name:
                item["qty"] += 1
                found = True
                break

        if not found:
            cart.append({
                "name": name,
                "price": price,
                "qty": 1
            })

        request.session["cart"] = cart
        request.session.modified = True

        total_count = sum(item["qty"] for item in cart)
        total_amount = sum(item["price"] * item["qty"] for item in cart)

        return JsonResponse({
            "cart": cart,
            "count": total_count,
            "total": total_amount
        })


def get_cart_data(request):
    cart = request.session.get("cart", [])
    total_count = sum(item["qty"] for item in cart)
    total_amount = sum(item["price"] * item["qty"] for item in cart)

    return JsonResponse({
        "cart": cart,
        "count": total_count,
        "total": total_amount
    })


def change_cart_qty(request):
    if request.method == "POST":
        data = json.loads(request.body)
        index = int(data.get("index"))
        change = int(data.get("change"))

        cart = request.session.get("cart", [])

        if 0 <= index < len(cart):
            cart[index]["qty"] += change
            if cart[index]["qty"] <= 0:
                cart.pop(index)

        request.session["cart"] = cart
        request.session.modified = True

        total_count = sum(item["qty"] for item in cart)
        total_amount = sum(item["price"] * item["qty"] for item in cart)

        return JsonResponse({
            "cart": cart,
            "count": total_count,
            "total": total_amount
        })

def remove_cart_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        index = int(data.get("index"))

        cart = request.session.get("cart", [])

        if 0 <= index < len(cart):
            cart.pop(index)

        request.session["cart"] = cart
        request.session.modified = True

        total_count = sum(item["qty"] for item in cart)
        total_amount = sum(item["price"] * item["qty"] for item in cart)

        return JsonResponse({
            "cart": cart,
            "count": total_count,
            "total": total_amount
        })

def order_success(request):
    return render(request, "order_success.html")

#-------------------------------------------------#
# Product list + add new product
def product_page(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        price = request.POST.get('price')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO product_db (Product_Name, Brand, Category, Price)
                VALUES (%s, %s, %s, %s)
            """, [product_name, brand, category, price])

        return redirect('product')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Product_ID, Product_Name, Brand, Category, Price
            FROM product_db
            ORDER BY Product_ID DESC
        """)
        products = cursor.fetchall()

    return render(request, 'product.html', {'products': products})

# Edit / Update product
def edit_product(request, product_id):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        price = request.POST.get('price')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE product_db
                SET Product_Name=%s, Brand=%s, Category=%s, Price=%s
                WHERE Product_ID=%s
            """, [product_name, brand, category, price, product_id])

        return redirect('product')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Product_ID, Product_Name, Brand, Category, Price
            FROM product_db
            WHERE Product_ID=%s
        """, [product_id])
        product = cursor.fetchone()

        cursor.execute("""
            SELECT Product_ID, Product_Name, Brand, Category, Price
            FROM product_db
            ORDER BY Product_ID DESC
        """)
        products = cursor.fetchall()

    return render(request, 'product.html', {
        'products': products,
        'edit_product': product
    })


# Delete product
def delete_product(request, product_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM product_db WHERE Product_ID=%s", [product_id])

    return redirect('product')

#.....admin feedback....#
def view_feedback(request):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="chatpata",
        port=3307,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    # Delete feedback
    delete_id = request.GET.get("delete")
    if delete_id:
        cursor.execute("DELETE FROM feedback WHERE Feedback_ID=%s", (delete_id,))
        conn.commit()
        conn.close()
        return redirect('view_feedback')

    # Fetch all feedbacks
    cursor.execute("SELECT * FROM feedback ORDER BY Feedback_ID DESC")
    feedbacks = cursor.fetchall()

    positive_words = [
        'good', 'very good', 'excellent', 'nice', 'best', 'awesome',
        'amazing', 'great', 'love', 'liked', 'super', 'fantastic',
        'thank', 'thanks', 'thank you', 'satisfied', 'happy'
    ]

    negative_words = [
        'bad', 'worst', 'poor', 'hate', 'useless', 'boring',
        'disappointed', 'slow', 'waste', 'problem', 'issue',
        'not good', 'not satisfied', 'dirty', 'late'
    ]

    def get_status(text, rating):
        text = str(text).lower().strip()
        rating = int(rating) if str(rating).isdigit() else 0
        if text == "":
            if rating >= 4:
                return "Positive"
            elif rating > 0 and rating <= 2:
                return "Negative"
            else:
                return "Pending"

        if any(word in text for word in negative_words):
            return "Negative"

        if any(word in text for word in positive_words):
            return "Positive"
        if rating >= 4:
            return "Positive"
        elif rating > 0 and rating <= 2:
            return "Negative"
        else:
            return "Pending"
    for f in feedbacks:
        f['Status'] = get_status(f.get('Feedback', ''), f.get('Rating', 0))
    positive_id = request.GET.get("positive")
    if positive_id:
        for f in feedbacks:
            if str(f['Feedback_ID']) == str(positive_id):
                f['Status'] = 'Positive'
                break

    total = len(feedbacks)
    positive_count = sum(1 for f in feedbacks if f['Status'] == 'Positive')
    negative_count = sum(1 for f in feedbacks if f['Status'] == 'Negative')
    pending_count = sum(1 for f in feedbacks if f['Status'] == 'Pending')

    conn.close()

    return render(request, 'view_feedback.html', {
        'feedbacks': feedbacks,
        'total': total,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'pending_count': pending_count,
    })
#.......manage categories........#
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="chatpata",
        port=3307,
        cursorclass=pymysql.cursors.DictCursor
    )

def admin_categories(request):
    

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        category_name = request.POST.get("category_name")
        category_image = request.POST.get("category_image")
        category_description = request.POST.get("category_description")
        status = request.POST.get("status")

        if not category_name:
            messages.error(request, "Category name required hai.")
        else:
            try:
                cursor.execute(
                    "INSERT INTO category_db (Category_Name, Category_Image, Category_Description, Status) VALUES (%s, %s, %s, %s)",
                    (category_name, category_image, category_description, status)
                    )
                conn.commit()
                messages.success(request, "Category successfully add ho gayi.")
                conn.close()
                return redirect('admin_categories')
            except Exception as e:
                messages.error(request, f"Error: {e}")

    cursor.execute("SELECT * FROM category_db ORDER BY Category_ID DESC")
    categories = cursor.fetchall()

    conn.close()
    return render(request, "ad_category.html", {"categories": categories})

def edit_category(request, category_id):
    if not request.session.get('admin_id'):
        return redirect('alogin')

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        category_name = request.POST.get("category_name")
        category_image = request.POST.get("category_image")
        category_description = request.POST.get("category_description")
        status = request.POST.get("status")

        cursor.execute("""
            UPDATE category_db
            SET Category_Name=%s, Category_Image=%s, Category_Description=%s, Status=%s
            WHERE Category_ID=%s
        """, (category_name, category_image, category_description, status, category_id))
        conn.commit()
        conn.close()
        messages.success(request, "Category update ho gayi.")
        return redirect('admin_categories')

    cursor.execute("SELECT * FROM category_db WHERE Category_ID=%s", (category_id,))
    category = cursor.fetchone()
    conn.close()

    return render(request, "edit_category.html", {"category": category})

def delete_category(request, category_id):
    if not request.session.get('admin_id'):
        return redirect('alogin')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM category_db WHERE Category_ID=%s", (category_id,))
    conn.commit()
    conn.close()

    messages.success(request, "Category delete ho gayi.")
    return redirect('admin_categories')

def show_categories(request):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category_db WHERE Status='Active' ORDER BY Category_Name ASC")
    categories = cursor.fetchall()
    conn.close()
    return render(request, "ad_category.html", {"categories": categories})

#feedback user
def feedback(request):
    if not request.session.get('user_id'):
        return redirect('bow')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Feedback_ID, Feedback, Rating, Status
            FROM feedback
            ORDER BY Feedback_ID DESC
        """)
        rows = cursor.fetchall()

    feedbacks = []
    for row in rows:
        feedbacks.append({
            'id': row[0],
            'comment': row[1],
            'rating': row[2],
            'status': row[3],
        })

    return render(request, 'feedback.html', {'feedbacks': feedbacks})



    

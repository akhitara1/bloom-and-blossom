from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum

from .models import (
    Product,
    Order,
    OrderItem,
    Category,
    Review
)


# =====================================================
# ADMIN REQUIRED
# =====================================================

def admin_required(view_func):

    return user_passes_test(
        lambda user: user.is_staff,
        login_url="/admin-login/"
    )(view_func)


# =====================================================
# HOME
# =====================================================

def home(request):

    products = Product.objects.all().order_by("-id")

    roses = Product.objects.filter(
        category__iexact="Roses"
    ).first()

    tulips = Product.objects.filter(
        category__iexact="Tulips"
    ).first()

    sunflowers = Product.objects.filter(
        category__iexact="Sunflowers"
    ).first()

    bouquets = Product.objects.filter(
        category__iexact="Bouquets"
    ).first()

    cart = request.session.get(
        "cart",
        {}
    )

    cart_count = sum(cart.values())

    return render(
        request,
        "index.html",
        {
            "products": products,
            "roses": roses,
            "tulips": tulips,
            "sunflowers": sunflowers,
            "bouquets": bouquets,
            "cart_count": cart_count
        }
    )


# =====================================================
# SHOP
# =====================================================

def shop(request):

    products = Product.objects.all().order_by("-id")

    cart = request.session.get(
        "cart",
        {}
    )

    cart_count = sum(cart.values())

    return render(
        request,
        "shop.html",
        {
            "products": products,
            "cart_count": cart_count
        }
    )


# =====================================================
# CATEGORY PRODUCTS
# =====================================================

def category_products(request, category_name):

    products = Product.objects.filter(
        category__iexact=category_name
    ).order_by("-id")

    cart = request.session.get(
        "cart",
        {}
    )

    cart_count = sum(cart.values())

    return render(
        request,
        "shop.html",
        {
            "products": products,
            "cart_count": cart_count,
            "selected_category": category_name
        }
    )


# =====================================================
# BLOG DETAIL
# =====================================================

def blog_detail(request, blog_id):

    blogs = {

        1: {
            "date": "March 12, 2026",
            "title": "How to Choose the Perfect Bouquet",
            "description": "Learn how to choose the right flowers for birthdays, anniversaries and other special occasions.",
            "image": "8.webp",
            "content": "Choosing the perfect bouquet depends on the occasion, the person receiving the flowers, and the message you want to express. A thoughtful bouquet can make any special moment more memorable."
        },

        2: {
            "date": "March 08, 2026",
            "title": "5 Flowers That Express Love",
            "description": "Discover beautiful flowers that can help you express love, friendship and heartfelt emotions.",
            "image": "7.jpg",
            "content": "Flowers are a beautiful way to express love, friendship and heartfelt emotions. Different flowers and colours can communicate different feelings and make a gift more meaningful."
        },

        3: {
            "date": "February 28, 2026",
            "title": "Simple Tips to Keep Flowers Fresh",
            "description": "Follow these simple tips to keep your beautiful bouquet fresh and vibrant for longer.",
            "image": "SereneWhiteLiliesinVase-1755149681540.webp",
            "content": "To keep flowers fresh, place them in clean water and keep them away from direct sunlight and excessive heat. Changing the water regularly can help flowers stay fresh for longer."
        }
    }

    blog = blogs.get(blog_id)

    if not blog:
        return redirect("home")

    return render(
        request,
        "blog_detail.html",
        {
            "blog": blog
        }
    )

    blogs = {

        1: {
            "date": "March 12, 2026",
            "title": "How to Choose the Perfect Bouquet",
            "description": (
                "Learn how to choose the right flowers "
                "for birthdays, anniversaries and other "
                "special occasions."
            ),
            "category": "Roses",
            "content": (
                "Choosing the perfect bouquet depends on "
                "the occasion, the person receiving the flowers, "
                "and the message you want to express. "
                "Roses are a classic choice for expressing love, "
                "while tulips can represent happiness and freshness. "
                "A mixed bouquet is also a wonderful choice when "
                "you want to create a colourful and cheerful gift."
            )
        },

        2: {
            "date": "March 08, 2026",
            "title": "5 Flowers That Express Love",
            "description": (
                "Discover beautiful flowers that can help "
                "you express love, friendship and heartfelt emotions."
            ),
            "category": "Bouquets",
            "content": (
                "Flowers are a beautiful way to express emotions. "
                "Red roses are traditionally associated with love. "
                "Tulips can represent caring and happiness, while "
                "mixed bouquets can communicate warmth and affection. "
                "Choosing the right flowers makes a gift more personal "
                "and memorable."
            )
        },

        3: {
            "date": "February 28, 2026",
            "title": "Simple Tips to Keep Flowers Fresh",
            "description": (
                "Follow these simple tips to keep your beautiful "
                "bouquet fresh and vibrant for longer."
            ),
            "category": "Sunflowers",
            "content": (
                "To keep flowers fresh, always place them in a "
                "clean vase with fresh water. Keep the flowers "
                "away from direct sunlight and excessive heat. "
                "Changing the water regularly and trimming the "
                "stems can also help your flowers stay fresh "
                "for a longer period of time."
            )
        }
    }

    blog = blogs.get(blog_id)

    if not blog:
        return redirect("home")

    # Find a real product image from the selected category
    product = Product.objects.filter(
        category__iexact=blog["category"]
    ).exclude(
        image=""
    ).first()

    return render(
        request,
        "blog_detail.html",
        {
            "blog": blog,
            "product": product
        }
    )


# =====================================================
# PRODUCT DETAIL
# =====================================================

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    reviews = Review.objects.filter(
        product=product
    ).order_by("-created_at")

    cart = request.session.get(
        "cart",
        {}
    )

    cart_count = sum(cart.values())

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "cart_count": cart_count
        }
    )


# =====================================================
# ADD TO CART
# =====================================================

def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product.stock > 0:

        if product_id in cart:

            if cart[product_id] < product.stock:

                cart[product_id] += 1

            else:

                messages.warning(
                    request,
                    f"Only {product.stock} "
                    f"{product.name} available."
                )

                request.session["cart"] = cart
                request.session.modified = True

                return redirect(
                    "product_detail",
                    product_id=product.id
                )

        else:

            cart[product_id] = 1

        request.session["cart"] = cart
        request.session.modified = True

        messages.success(
            request,
            f"{product.name} added to cart successfully!"
        )

    else:

        messages.error(
            request,
            f"{product.name} is currently out of stock."
        )

    return redirect(
        "product_detail",
        product_id=product.id
    )


# =====================================================
# CART
# =====================================================

def cart(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    products = []
    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        subtotal = product.price * quantity

        total += subtotal

        products.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            }
        )

    cart_count = sum(cart_data.values())

    return render(
        request,
        "cart.html",
        {
            "products": products,
            "total": total,
            "cart_count": cart_count
        }
    )


# =====================================================
# INCREASE QUANTITY
# =====================================================

def increase_quantity(request, product_id):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart:

        product = get_object_or_404(
            Product,
            id=product_id
        )

        if cart[product_id] < product.stock:
            cart[product_id] += 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


# =====================================================
# DECREASE QUANTITY
# =====================================================

def decrease_quantity(request, product_id):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart:

        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


# =====================================================
# REMOVE FROM CART
# =====================================================

def remove_from_cart(request, product_id):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


# =====================================================
# CHECKOUT
# =====================================================

def checkout(request):

    if not request.user.is_authenticated:

        messages.warning(
            request,
            "Please login before placing an order."
        )

        return redirect("customer_login")

    cart_data = request.session.get(
        "cart",
        {}
    )

    products = []
    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        subtotal = product.price * quantity

        total += subtotal

        products.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            }
        )

    if not products:
        return redirect("cart")

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        division = request.POST.get("division")
        district = request.POST.get("district")
        payment_method = request.POST.get("payment_method")
        bkash_number = request.POST.get("bkash_number")
        transaction_id = request.POST.get("transaction_id")

        if not name:
            messages.error(
                request,
                "Please enter your name."
            )
            return redirect("checkout")

        if not phone:
            messages.error(
                request,
                "Please enter your phone number."
            )
            return redirect("checkout")

        if not address:
            messages.error(
                request,
                "Please enter your delivery address."
            )
            return redirect("checkout")

        if not division:
            messages.error(
                request,
                "Please select your division."
            )
            return redirect("checkout")

        if not district:
            messages.error(
                request,
                "Please select your district."
            )
            return redirect("checkout")

        if not payment_method:
            messages.error(
                request,
                "Please select a payment method."
            )
            return redirect("checkout")

        if payment_method == "bKash":

            if not bkash_number:
                messages.error(
                    request,
                    "Please enter your bKash number."
                )
                return redirect("checkout")

            if not transaction_id:
                messages.error(
                    request,
                    "Please enter your bKash Transaction ID."
                )
                return redirect("checkout")

        for item in products:

            product = item["product"]
            quantity = item["quantity"]

            if product.stock < quantity:

                messages.error(
                    request,
                    f"Sorry! Only {product.stock} "
                    f"{product.name} available."
                )

                return redirect("cart")

        order = Order.objects.create(

            user=request.user,

            name=name,

            phone=phone,

            address=address,

            division=division,

            district=district,

            payment_method=payment_method,

            bkash_number=(
                bkash_number
                if payment_method == "bKash"
                else ""
            ),

            transaction_id=(
                transaction_id
                if payment_method == "bKash"
                else ""
            ),

            total=total,

            status="Pending"
        )

        for item in products:

            product = item["product"]
            quantity = item["quantity"]
            subtotal = item["subtotal"]

            OrderItem.objects.create(

                order=order,

                product=product,

                quantity=quantity,

                price=product.price,

                subtotal=subtotal
            )

            product.stock -= quantity
            product.save()

        request.session["cart"] = {}
        request.session.modified = True

        messages.success(
            request,
            f"Order #{order.id} placed successfully!"
        )

        return redirect("order_success")

    return render(
        request,
        "checkout.html",
        {
            "products": products,
            "total": total
        }
    )


# =====================================================
# ORDER SUCCESS
# =====================================================

def order_success(request):

    return render(
        request,
        "order_success.html"
    )


# =====================================================
# CUSTOMER REGISTER
# =====================================================

def register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("register")

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "This username is already taken."
            )

            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = name
        user.save()

        login(request, user)

        messages.success(
            request,
            "Account created successfully!"
        )

        return redirect("dashboard")

    return render(
        request,
        "register.html"
    )


# =====================================================
# CUSTOMER LOGIN
# =====================================================

def customer_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                "Login successful!"
            )

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

        return redirect("customer_login")

    return render(
        request,
        "login.html"
    )


# =====================================================
# CUSTOMER LOGOUT
# =====================================================

def customer_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("customer_login")


# =====================================================
# CUSTOMER DASHBOARD
# =====================================================

def dashboard(request):

    if not request.user.is_authenticated:

        return redirect("customer_login")

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    total_orders = orders.count()

    pending_orders = orders.filter(
        status="Pending"
    ).count()

    total_spent = sum(
        order.total
        for order in orders
    )

    return render(
        request,
        "dashboard.html",
        {
            "orders": orders[:10],
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "total_spent": total_spent
        }
    )


# =====================================================
# ADMIN LOGIN
# =====================================================

def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_staff:

                login(request, user)

                return redirect("admin_dashboard")

            else:

                messages.error(
                    request,
                    "You are not authorized as an admin."
                )

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "admin_login.html"
    )


# =====================================================
# ADMIN DASHBOARD
# =====================================================

@admin_required
def admin_dashboard(request):

    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    total_customers = User.objects.filter(
        is_staff=False
    ).count()

    total_sales = Order.objects.aggregate(
        total=Sum("total")
    )["total"] or 0

    recent_orders = Order.objects.order_by(
        "-id"
    )[:5]

    products = Product.objects.all().order_by(
        "-id"
    )[:5]

    return render(
        request,
        "admin_dashboard.html",
        {
            "total_products": total_products,
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_sales": total_sales,
            "recent_orders": recent_orders,
            "products": products
        }
    )


# =====================================================
# ADMIN PRODUCT MANAGEMENT
# =====================================================

@admin_required
def admin_products(request):

    products = Product.objects.all().order_by("-id")

    return render(
        request,
        "admin_products.html",
        {
            "products": products
        }
    )


# =====================================================
# ADMIN ADD PRODUCT
# =====================================================

@admin_required
def admin_add_product(request):

    if request.method == "POST":

        name = request.POST.get("name")
        category = request.POST.get("category")
        price = request.POST.get("price")
        description = request.POST.get("description")
        stock = request.POST.get("stock")
        emoji = request.POST.get("emoji") or "💐"
        image = request.FILES.get("image")

        Product.objects.create(

            name=name,

            category=category,

            price=price,

            description=description,

            stock=stock,

            emoji=emoji,

            image=image
        )

        messages.success(
            request,
            f"{name} added successfully!"
        )

        return redirect("admin_products")

    categories = Category.objects.all().order_by("name")

    return render(
        request,
        "admin_add_product.html",
        {
            "categories": categories
        }
    )


# =====================================================
# ADMIN EDIT PRODUCT
# =====================================================

@admin_required
def admin_edit_product(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        product.name = request.POST.get("name")
        product.category = request.POST.get("category")
        product.price = request.POST.get("price")
        product.description = request.POST.get("description")
        product.stock = request.POST.get("stock")

        product.emoji = (
            request.POST.get("emoji")
            or "💐"
        )

        product.save()

        messages.success(
            request,
            f"{product.name} updated successfully!"
        )

        return redirect("admin_products")

    return render(
        request,
        "admin_edit_product.html",
        {
            "product": product
        }
    )


# =====================================================
# ADMIN DELETE PRODUCT
# =====================================================

@admin_required
def admin_delete_product(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Product deleted successfully!"
        )

    return redirect("admin_products")


# =====================================================
# ADD NEW CATEGORY
# =====================================================

@admin_required
def admin_add_category(request):

    if request.method == "POST":

        category_name = request.POST.get("name")

        if category_name:

            category_name = category_name.strip()

            if category_name:

                Category.objects.get_or_create(
                    name=category_name
                )

                messages.success(
                    request,
                    f"{category_name} category added successfully!"
                )

    return redirect("admin_add_product")


# =====================================================
# ADMIN ORDERS
# =====================================================

@admin_required
def admin_orders(request):

    orders = Order.objects.all().order_by(
        "-created_at"
    )

    pending_count = Order.objects.filter(
        status="Pending"
    ).count()

    processing_count = Order.objects.filter(
        status="Processing"
    ).count()

    shipped_count = Order.objects.filter(
        status="Shipped"
    ).count()

    delivered_count = Order.objects.filter(
        status="Delivered"
    ).count()

    return render(
        request,
        "admin_orders.html",
        {
            "orders": orders,
            "pending_count": pending_count,
            "processing_count": processing_count,
            "shipped_count": shipped_count,
            "delivered_count": delivered_count
        }
    )


# =====================================================
# ADMIN ORDER DETAIL
# =====================================================

@admin_required
def admin_order_detail(
    request,
    order_id
):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        "admin_order_detail.html",
        {
            "order": order
        }
    )


# =====================================================
# ADMIN UPDATE ORDER STATUS
# =====================================================

@admin_required
def admin_update_order_status(
    request,
    order_id
):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        new_status = request.POST.get("status")

        old_status = order.status

        if (
            new_status == "Cancelled"
            and old_status != "Cancelled"
        ):

            for item in order.items.all():

                if item.product:

                    item.product.stock += item.quantity
                    item.product.save()

        elif (
            old_status == "Cancelled"
            and new_status != "Cancelled"
        ):

            for item in order.items.all():

                if item.product:

                    if item.product.stock >= item.quantity:

                        item.product.stock -= item.quantity
                        item.product.save()

                    else:

                        messages.error(
                            request,
                            f"Not enough stock for "
                            f"{item.product.name}."
                        )

                        return redirect(
                            "admin_order_detail",
                            order_id=order.id
                        )

        order.status = new_status
        order.save()

        messages.success(
            request,
            f"Order #{order.id} status updated "
            f"to {new_status}."
        )

    return redirect(
        "admin_order_detail",
        order_id=order.id
    )


# =====================================================
# ADD PRODUCT REVIEW
# =====================================================

def add_review(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        name = request.POST.get("name")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if name and rating and comment:

            try:
                rating = int(rating)

            except ValueError:
                rating = 0

            if rating < 1 or rating > 5:

                messages.error(
                    request,
                    "Rating must be between 1 and 5."
                )

                return redirect(
                    "product_detail",
                    product_id=product.id
                )

            Review.objects.create(

                product=product,

                user=(
                    request.user
                    if request.user.is_authenticated
                    else None
                ),

                name=name,

                rating=rating,

                comment=comment
            )

            messages.success(
                request,
                "Your review has been added successfully!"
            )

        else:

            messages.error(
                request,
                "Please fill in all review fields."
            )

    return redirect(
        "product_detail",
        product_id=product.id
    )
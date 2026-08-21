from django.urls import path

from . import views


urlpatterns = [

    # HOME
    path(
        "",
        views.home,
        name="home"
    ),

    # SHOP
    path(
        "shop/",
        views.shop,
        name="shop"
    ),

    # PRODUCT DETAIL
    path(
        "product/<int:product_id>/",
        views.product_detail,
        name="product_detail"
    ),

    # CART
    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    # ADD TO CART
    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    # INCREASE
    path(
        "cart/increase/<int:product_id>/",
        views.increase_quantity,
        name="increase_quantity"
    ),

    # DECREASE
    path(
        "cart/decrease/<int:product_id>/",
        views.decrease_quantity,
        name="decrease_quantity"
    ),

    # REMOVE
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    # CHECKOUT
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    # ORDER SUCCESS
    path(
        "order-success/",
        views.order_success,
        name="order_success"
    ),

    # REGISTER
    path(
        "register/",
        views.register,
        name="register"
    ),

    # LOGIN
    path(
        "login/",
        views.customer_login,
        name="customer_login"
    ),

    # LOGOUT
    path(
        "logout/",
        views.customer_logout,
        name="customer_logout"
    ),

    # CUSTOMER DASHBOARD
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),
    path(
    "admin-login/",
    views.admin_login,
    name="admin_login"
),

path(
    "admin-dashboard/",
    views.admin_dashboard,
    name="admin_dashboard"
),
path(
    "admin-products/",
    views.admin_products,
    name="admin_products"
),

path(
    "admin-products/add/",
    views.admin_add_product,
    name="admin_add_product"
),

path(
    "admin-products/edit/<int:product_id>/",
    views.admin_edit_product,
    name="admin_edit_product"
),

path(
    "admin-products/delete/<int:product_id>/",
    views.admin_delete_product,
    name="admin_delete_product"
),
path(
    "admin-products/add-category/",
    views.admin_add_category,
    name="admin_add_category"
),
path(
    "admin-orders/",
    views.admin_orders,
    name="admin_orders"
),

path(
    "admin-orders/<int:order_id>/",
    views.admin_order_detail,
    name="admin_order_detail"
),

path(
    "admin-orders/<int:order_id>/status/",
    views.admin_update_order_status,
    name="admin_update_order_status"
),
path(
    "product/<int:product_id>/review/",
    views.add_review,
    name="add_review"
),

]
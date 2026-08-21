from django.db import models
from django.contrib.auth.models import User


# =========================
# CATEGORY
# =========================

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# =========================
# PRODUCT
# =========================

class Product(models.Model):

    name = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=100
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    stock = models.IntegerField(
        default=0
    )
    image = models.ImageField(
    upload_to="products/",
    blank=True,
    null=True
    )

    emoji = models.CharField(
        max_length=10,
        default="💐"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =========================
# ORDER
# =========================

class Order(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    division = models.CharField(
        max_length=50
    )

    district = models.CharField(
        max_length=50
    )

    payment_method = models.CharField(
        max_length=50
    )
    bkash_number = models.CharField(
    max_length=20,
    null=True,
    blank=True
    )

    transaction_id = models.CharField(
    max_length=100,
    null=True,
    blank=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    def __str__(self):

        return f"Order #{self.id} - {self.name}"


# =========================
# ORDER ITEM
# =========================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):

        product_name = (
            self.product.name
            if self.product
            else "Deleted Product"
        )

        return f"{product_name} × {self.quantity}"
    # =========================
# PRODUCT REVIEW
# =========================

class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    rating = models.PositiveIntegerField(
        default=5
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.product.name} - {self.rating} Stars"
   
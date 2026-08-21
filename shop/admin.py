from django.contrib import admin

from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "stock",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "phone",
        "district",
        "total",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "division",
        "district",
    )

    search_fields = (
        "name",
        "phone",
        "district",
    )

    ordering = (
        "-created_at",
    )
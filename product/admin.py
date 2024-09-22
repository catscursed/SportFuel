from django.contrib import admin
from .models import Banner, Brand, Category, Product, Storage, Image, Like, User, Basket

# Регистрация моделей
admin.site.register(Banner)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Storage)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(User)
admin.site.register(Basket)

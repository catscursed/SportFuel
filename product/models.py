from django.contrib.auth import get_user_model
from django.db import models
import uuid

User = get_user_model()


class Brand(models.Model):
    logo = models.ImageField(upload_to='media/brand_logo')
    title = models.CharField(max_length=123)

    def __str__(self):
        return self.title


class Image(models.Model):
    file = models.ImageField(upload_to='media/image')


class Category(models.Model):
    title = models.CharField(max_length=223)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField()
    country = models.CharField(max_length=123)
    volume = models.CharField(max_length=20)
    release_form = models.CharField(max_length=123)
    number_of_servings = models.PositiveSmallIntegerField()
    actual_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    main_photo = models.ImageField(upload_to='media/main_photo')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    brands = models.ManyToManyField(Brand)
    categories = models.ManyToManyField(Category)
    images = models.ManyToManyField(Image)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Storage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Нет в наличие'),
            (2, 'Скоро в наличии'),
            (3, 'В наличии')
        )
    )
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    description = models.CharField(max_length=123)
    is_main = models.BooleanField()

    def __str__(self):
        return str(self.product)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.product}"


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Storage, on_delete=models.CASCADE)
    delivery_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=500.00
    )
    quantity = models.PositiveSmallIntegerField()
    unique_code = models.CharField(max_length=40, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True, blank=True, null=True)
    shipping_date = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=223)
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'В пути'),
            (2, 'Доставлен'),
            (3, 'Отменен'),
            (4, 'В обработке')
        ),
        default=4
    )
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4())[:8]
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

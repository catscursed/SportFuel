from rest_framework import serializers
from .models import Brand, Image, Like, Category, Product, Storage, Banner, Basket


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'title', 'logo')

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')

class ProductListSerializer(serializers.ModelSerializer):
    brands = BrandListSerializer(many=True)  # Изменение: добавлено поле brands с many=True

    class Meta:
        model = Product
        fields = ('id', 'title', 'brands', 'country', 'release_form', 'number_of_servings', 'actual_price')  # Изменение: добавлено поле brands в fields

class ProductActionListSerializer(serializers.ModelSerializer):
    brands = BrandListSerializer(many=True)  # Изменение: добавлено поле brands с many=True

    class Meta:
        model = Product
        fields = ('id', 'title', 'brands', 'country', 'release_form', 'number_of_servings', 'actual_price', 'old_price')  # Изменение: добавлено поле brands в fields

class StorageListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = Storage
        fields = ('id', 'product', 'get_status_display', 'created_date')

class StorageActionListSerializer(serializers.ModelSerializer):
    product = ProductActionListSerializer()

    class Meta:
        model = Storage
        fields = ('id', 'product', 'get_status_display', 'created_date')

class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('file',)

class BannerListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    image = ImageListSerializer()

    class Meta:
        model = Banner
        fields = ('id', 'product', 'image', 'description', 'is_main')

class ProductDetailListSerializer(serializers.ModelSerializer):
    categories = CategoryListSerializer(many=True)  # Изменение: правильное именование поля categories
    brands = BrandListSerializer(many=True)
    images = ImageListSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

class StorageDetailListSerializer(serializers.ModelSerializer):
    product = ProductDetailListSerializer()

    class Meta:
        model = Storage
        fields = ('id', 'product', 'quantity', 'get_status_display', 'created_date', 'update_date')


class LikeCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('user', 'product')


class BasketCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Basket
        fields = ('user', 'product', 'quantity', 'address')

    def validate(self, attrs):
        product_id = attrs['product'].id

        if not Storage.objects.filter(id=product_id).exists():
            raise serializers.ValidationError('Такого товара не существует!')

        return attrs

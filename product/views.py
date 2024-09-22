from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView

from .filters import StorageListFilter
from .models import Brand, Image, Category, Product, Banner, Storage, Like
from .serializers import (
    BrandListSerializer,
    CategoryListSerializer,
    ProductListSerializer,
    ProductActionListSerializer,
    ImageListSerializer,
    BannerListSerializer,
    StorageListSerializer,
    StorageActionListSerializer,
    StorageDetailListSerializer,
    LikeCreateSerializer,
    BasketCreateSerializer
)


class MainPageView(APIView):
    def get(self, request):
        banners = Banner.objects.all()
        categories = Category.objects.all()
        bestsellers = Storage.objects.all()
        action_products = Storage.objects.filter(product__old_price__gt=F('product__actual_price'))

        banners_serializers = BannerListSerializer(banners, many=True)
        categories_serializer = CategoryListSerializer(categories, many=True)
        bestsellers_serializers = StorageListSerializer(bestsellers, many=True)
        action_products_serializers = StorageActionListSerializer(action_products, many=True)

        data = {
            'banners': banners_serializers.data,
            'categories': categories_serializer.data,
            'bestsellers': bestsellers_serializers.data,
            'action_products': action_products_serializers.data
        }
        return Response(data)


class StorageDetailListView(APIView):
    def get(self, request, slug):

        product_detail = Storage.objects.filter(product__slug=slug).first()
        if not product_detail:
            return Response({'error': 'Product not found'}, status=404)
        similar = Storage.objects.filter(product__categories__in=product_detail.product.categories.all()).exclude(id=product_detail.id).distinct()

        product_serializer = StorageDetailListSerializer(product_detail)
        similar_serializer = StorageListSerializer(similar, many=True)

        data = {
            'cap_detail': product_serializer.data,
            'similar': similar_serializer.data
        }
        return Response(data)

    def post(self, request, slug):
        serializer = LikeCreateSerializer(data=request.data, context={'request' : request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)


class StorageListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListView(ListCreateAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StorageListFilter
    pagination_class = StorageListPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StorageListSerializer
        elif self.request.method == 'POST':
            return LikeCreateSerializer


class BasketCreateView(CreateAPIView):
    permission_classes =[IsAuthenticated]

    def post(self, request):
        serializer = BasketCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)



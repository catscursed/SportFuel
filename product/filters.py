import django_filters
from .models import Storage


class StorageListFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='product__actual_price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='product__actual_price', lookup_expr='lt')

    class Meta:
        model = Storage
        fields = {
            'product__title': ['exact', 'icontains'],
            'product__brands': ['exact'],
            'product__country': ['exact'],
            'product__categories': ['exact'],
            'status': ['exact'],
        }

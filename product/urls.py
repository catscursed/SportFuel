from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.MainPageView.as_view()),
    path('product_detail/<slug:slug>/', views.StorageDetailListView.as_view()),
    path('product_list/', views.ProductListView.as_view()),
    path('buy_product/', views.BasketCreateView.as_view()),

]

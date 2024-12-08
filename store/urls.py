from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'

urlpatterns = [
    # Главная страница
    path('main/', views.main_page, name='main_page'),

    # URL для регионов
    path('regions/', views.region_list, name='region_list'),
    path('regions/create/', views.region_create, name='region_create'),
    path('regions/<int:id>/edit/', views.region_edit, name='region_edit'),
    path('regions/<int:id>/delete/', views.region_delete, name='region_delete'),

    # URL для покупателей
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:id>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:id>/delete/', views.customer_delete, name='customer_delete'),

    # Динамическая загрузка покупателей по региону (JSON-ответ)
    path('region/<int:region_id>/customers/', views.customers_by_region, name='customers_by_region'),

    # URL для покупок
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('purchases/create/', views.purchase_create, name='purchase_create'),
    path('purchase/<int:customer_id>/', views.purchase, name='purchase'),  # маршрут для оформления покупки
]

# Добавление маршрутов для статических файлов (например, изображений)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

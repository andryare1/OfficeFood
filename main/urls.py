from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'main'


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.get_user_profile, name='profile'),
    path('menu/', views.menu, name='menu'),
    path('export-statistics/', views.export_statistics, name='export_statistics'),
    path('product-statistics/', views.product_statistics, name='product_statistics'),
    path('export-product-statistics/', views.export_product_statistics, name='export_product_statistics'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

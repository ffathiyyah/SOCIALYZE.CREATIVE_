
from django.urls import path
from . import views

urlpatterns = [
    # HALAMAN UTAMA
    path('', views.home, name='home'),
    path('artikel/', views.public_articles, name='public_articles'),
    path(
        'artikel/<slug:slug>/',
        views.public_article_detail,
        name='public_article_detail'
    ),

    # AUTENTIKASI
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.staff_logout, name='staff_logout'),
    path('staff-login/', views.staff_login, name='staff_login'),

    # DASHBOARD ADMIN
    path('dashboard/', views.dashboard, name='dashboard'),

    # KELOLA ARTIKEL
    path(
        'dashboard/articles/',
        views.admin_articles,
        name='admin_articles'
    ),
    path(
        'dashboard/articles/add/',
        views.admin_article_create,
        name='admin_article_create'
    ),
    path(
        'dashboard/articles/<int:article_id>/edit/',
        views.admin_article_edit,
        name='admin_article_edit'
    ),
    path(
        'dashboard/articles/<int:article_id>/preview/',
        views.admin_article_preview,
        name='admin_article_preview'
    ),
    path(
        'dashboard/articles/<int:article_id>/publish/',
        views.admin_article_publish,
        name='admin_article_publish'
    ),
    path(
        'dashboard/articles/<int:article_id>/unpublish/',
        views.admin_article_unpublish,
        name='admin_article_unpublish'
    ),
    path(
        'dashboard/articles/<int:article_id>/delete/',
        views.admin_article_delete,
        name='admin_article_delete'
    ),

    # KELOLA LAYANAN
    path(
        'dashboard/services/',
        views.admin_services,
        name='admin_services'
    ),
    path(
        'dashboard/services/add/',
        views.admin_service_create,
        name='admin_service_create'
    ),
    path(
        'dashboard/services/<int:service_id>/edit/',
        views.admin_service_edit,
        name='admin_service_edit'
    ),
    path(
        'dashboard/services/<int:service_id>/delete/',
        views.admin_service_delete,
        name='admin_service_delete'
    ),

    # DASHBOARD PENGGUNA
    path('my-dashboard/', views.user_dashboard, name='user_dashboard'),

    # PROFIL ADMIN
    path('admin-profile/', views.admin_profile, name='admin_profile'),

    # API PESANAN
path('api/orders/', views.orders_api, name='orders_api'),

path(
    'api/midtrans/notification/',
    views.midtrans_webhook,
    name='midtrans_webhook'
),

path(
    'api/orders/<int:order_id>/',
    views.order_detail_api,
    name='order_detail_api'
),

    # API KONSULTASI
    path(
        'api/consultations/',
        views.submit_consultation,
        name='consultations_api'
    ),
    path(
        'api/admin/consultations/',
        views.consultations_api,
        name='admin_consultations_api'
    ),

    # PENGELOLAAN PESANAN
    path(
        'dashboard/orders/<int:order_id>/status/',
        views.update_order_status,
        name='update_order_status'
    ),
    path(
        'dashboard/orders/<int:order_id>/delete/',
        views.delete_order,
        name='delete_order'
    ),
]
 
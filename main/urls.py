from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.my_dashboard, name='my_dashboard'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('marketplace/', views.product_list, name='product_list'),
    path('marketplace/create/', views.product_create, name='product_create'),
    path('marketplace/<slug:slug>/', views.product_detail, name='product_detail'),
    path('marketplace/<slug:slug>/buy/', views.create_order, name='create_order'),
    path('orders/<int:order_id>/pay/', views.order_pay, name='order_pay'),
    path('forum/', views.forum_list, name='forum_list'),
    path('forum/create/', views.forum_topic_create, name='forum_topic_create'),
    path('forum/topic/<int:pk>/', views.forum_topic_detail, name='forum_topic_detail'),
    path('bootstrap-demo/', views.bootstrap_demo, name='bootstrap_demo'),
]

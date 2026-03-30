from django.contrib import admin
from django.urls import path
from web import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('nontypes/', views.nontype, name='nontypes'),
    path('adven/', views.adven, name='adven'),
    path('dare/', views.dare, name='dare'),
    path('humble/', views.humble, name='humble'),
    path('care/', views.care, name='care'),
    path('topa/', views.topa, name='topa'),
    path('hero/', views.hero, name='hero'),
    path('pagal/', views.pagal, name='pagal'),
    path('bby/', views.bby, name='bby'),
    path('each/', views.each, name='each'),
    path('pen/', views.pen, name='pen'),
    path('scale/', views.scale, name='scale'),
    path('book/', views.book, name='book'),
    path('comb/', views.comb, name='comb'),
    path('now/', views.now, name='now'),
    path('phn/', views.phn, name='phn'),
    path('paper/', views.paper, name='paper'),
    path('dell/', views.dell, name='dell'),
    path('hp/', views.hp, name='hp'),
    path('register/', views.register, name='register'),
    path('bow/', views.bow, name='bow'),
    path('logout/', views.logout, name='logout'),
    path('boat/', views.boat, name='boat'),
    path('sec/', views.sec, name='sec'),
    path('kok/', views.kok, name='kok'),
    path('order-success/', views.order_success, name='order_success'),


#user
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.orders, name='orders'),
    path('payment/', views.payment, name='payment'),
    path('sidebar/', views.sidebar, name='sidebar'),
    path('ad_feedback/', views.ad_feedback, name='ad_feedback'),

#admin
    path('alogin/', views.alogin, name='alogin'),
    path('adashboard/', views.adashboard, name='adashboard'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('get-cart-data/', views.get_cart_data, name='get_cart_data'),
    path('change-cart-qty/', views.change_cart_qty, name='change_cart_qty'),
    path('remove-cart-item/', views.remove_cart_item, name='remove_cart_item'),
    path('view_feedback/', views.view_feedback, name='view_feedback'),
    path('users/', views.users, name='users'),
    path('view-user/<int:customer_id>/', views.view_user, name='view_user'),
    path('block-user/<int:customer_id>/', views.block_user, name='block_user'),
    path('aorders/', views.aorders, name='aorders'),
    path('apayment/', views.apayment, name='apayment'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('product/', views.product_page, name='product'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admin_category/', views.admin_categories, name='admin_categories'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('feedback/', views.feedback, name='feedback'),

]

 


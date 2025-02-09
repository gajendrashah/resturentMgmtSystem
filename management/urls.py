from django.urls import path
from .admin import SaleAdmin
from . import views

urlpatterns = [
    path('admin/print_sale/<int:pk>/', views.print_sale, name='print_sale'),
    path('kasjhfkajsdhf/', views.dashboard, name='dashboard'),
    path('', views.orderManagement, name='tableOrder'),
    path('api/create-order/', views.create_order, name='create_order'),
    path('purchase/', views.PurchaseItems, name='purchase'),
    path('edit_purchase/<int:purchase_id>/', views.edit_purchase, name='edit_purchase'),
    path('delete_purchase/<int:purchase_id>/', views.delete_purchase, name='delete_purchase'),
    path('room_order/', views.room_order, name='room_order'),
    path('room_order/api/create-order-room/', views.create_order_room, name='create_order_room'),
    path('room/advance/', views.roomDetail, name="advance" ),
    path('add-advance/<int:customer_id>/', views.add_advance, name='add_advance'),
]
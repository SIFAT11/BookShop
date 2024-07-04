from django.urls import path
from .views import *

urlpatterns = [
    path('SellBook', sell_book, name='SellBook'),
    path('viewbook/<str:book_id>/',viewbook, name='view_book'),
    path('bookrequest/<str:book_id>/', book_request, name='book_request'),
    path('cart/', cart, name='cart'), 
    path('add-to-cart/<str:book_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-quantity/<int:cart_item_id>/', update_quantity, name='update_quantity'),
    path('book_status/',Book_status, name='Book_status'),
    path('checkout/', checkout, name='checkout'),
     
]
    
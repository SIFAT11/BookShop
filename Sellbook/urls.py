from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('category/<int:category_id>/', category_books, name='category_books'),
    path('profile/', profile, name='profile'),
    path('membership/', membership_view, name='membership'),
    path('SellBook/', SellBook_option, name='SellBook'),
    path('seller_registration/', seller_registration, name='seller_registration'),
    path('seller_login/', seller_login, name='seller_login'),
    path('seller_profile/', seller_profile, name='seller_profile'),
    path('BookList/', Booklist, name='booklist'),
]

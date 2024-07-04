from django.db import models
from Sellbook.models import Seller_Profile
from Sellbook.models import Profile
from django.utils import timezone
import random
import string
import uuid
class Category(models.Model):
    category_ID= models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name
    

def generate_book_id():
        return f"{random.randint(10, 99)}{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}"
class Book(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]
    Book_ID = models.CharField(max_length=4, unique=True, default=generate_book_id)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)  # Corrected the keyword here
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(upload_to='book_covers', blank=True)
    quantity = models.PositiveSmallIntegerField()
    categories = models.ManyToManyField(Category)
    language = models.CharField(max_length=50)
    seller_profile = models.ForeignKey(Seller_Profile, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    condition = models.CharField(max_length=4, choices=CONDITION_CHOICES, default='none')
    description = models.TextField()
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.Book_ID:  # Generate a Book ID only if it's not set
            self.Book_ID = generate_book_id()
        super().save(*args, **kwargs)

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Book, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=100.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Convert delivery_charge to a Decimal object
        delivery_charge_decimal = Decimal(str(self.delivery_charge))

        # Calculate the subtotal based on the quantity and price of the associated book
        self.subtotal = self.book.price * self.quantity

        # Calculate the total amount by adding the subtotal and delivery charge
        self.total_amount = self.subtotal + delivery_charge_decimal

        super().save(*args, **kwargs)
        
        


class BookRequest(models.Model):
    REQUEST_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email = models.EmailField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    pickup_location = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    seller_profile = models.ForeignKey(Seller_Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.full_name} - {self.get_status_display()}"


from django.db import models
from dateutil.relativedelta import relativedelta
from django.utils import timezone

class Membership(models.Model):
    MONTHLY = 'Monthly'
    YEARLY = 'Yearly'
    
    PLAN_CHOICES = [
        (MONTHLY, 'Monthly'),
        (YEARLY, 'Yearly'),
    ]
    
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    membership_start_date = models.DateField(null=True, blank=True)
    membership_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        if self.plan == self.MONTHLY:
            return f"Monthly Membership - {self.get_status_display()}"
        elif self.plan == self.YEARLY:
            return f"Yearly Membership - {self.get_status_display()}"
        else:
            return "Invalid Membership Plan"

    def save(self, *args, **kwargs):
        if self.membership_start_date is None:
            self.membership_start_date = timezone.now().date()
            
            if self.plan == self.MONTHLY:
                self.membership_end_date = self.membership_start_date + relativedelta(months=1)
            elif self.plan == self.YEARLY:
                self.membership_end_date = self.membership_start_date + relativedelta(years=1)
        
        super().save(*args, **kwargs)


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100, default='')
    lname = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=100, blank=True)
    city_town = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode_zip = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    order_notes = models.TextField(max_length=300, default='No notes')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ({self.payment_status})"
 
    def get_order_id(self):
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"{self.id}{random_string}#"
    get_order_id.short_description = 'Order ID'



from django.db import models
from .models import Order, Book
from django.utils.html import mark_safe

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.price = self.book.price
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)
        
    def book_cover(self):
        return mark_safe(f'<img src="{self.book.cover.url}" alt="{self.book.title}" style="max-width: 100px; max-height: 100px;" />')
    book_cover.short_description = 'Book Cover'

    def book_id(self):
        return self.book.Book_ID
    book_id.short_description = 'Book ID'

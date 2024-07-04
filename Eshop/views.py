from django.shortcuts import render, redirect
from .models import Book, Category
from django.shortcuts import get_object_or_404
from .models import CartItem, Cart
from .models import CartItem
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import BookRequest

@login_required(login_url='seller_login')
def sell_book(request):
    if request.method == 'POST':
        # Extract book details from the form
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        cover = request.FILES.get('cover')
        quantity = request.POST.get('quantity')
        language = request.POST.get('language')
        location = request.POST.get('location')
        condition = request.POST.get('condition')
        description = request.POST.get('description')
        
        # Assuming you have a Seller_Profile object associated with the current user
        seller_profile = request.user.seller_profile
        
        # Extract the selected category ID from the form
        category_id = request.POST.get('category')
        
        # Fetch the corresponding category object
        category = Category.objects.get(pk=category_id)
        
        # Create the Book object with the selected category
        book = Book.objects.create(
            title=title,
            author=author,
            price=price,
            cover=cover,
            quantity=quantity,
            language=language,
            seller_profile=seller_profile,
            location=location,
            condition=condition,
            description=description
        )
        
        # Associate the book with the selected category
        book.categories.add(category)
        
        # Redirect to a success page or any other page
        return redirect('home')

    # If the request method is GET, render the sellbook.html template
    # and pass all categories to the template
    categories = Category.objects.all()
    return render(request, 'sellbook.html', {'categories': categories})


@login_required(login_url='Login')
def viewbook(request, book_id):
    book = get_object_or_404(Book, Book_ID=book_id)
    books = Book.objects.all()
    profile = request.user.profile
    try:
        membership = Membership.objects.get(profile=profile)
    except Membership.DoesNotExist:
        return render(request, 'ViewBookId.html', {'profile': profile, 'book': book})
    
    # Pass the book, books queryset, and membership to the template
    return render(request, 'ViewBookId.html', {'book': book, 'books': books, 'membership': membership})


from django.contrib.auth.decorators import login_required
from django.db.models import Sum



from decimal import Decimal


@login_required(login_url='Login')
def add_to_cart(request, book_id):
    if request.user.is_authenticated:
        book = Book.objects.get(Book_ID=book_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if the book is already in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={
                'quantity': 1,
                'delivery_charge': 100.0,
                'price': book.price,
                'subtotal': book.price,
                'total_amount': book.price + Decimal('100.0')
            }
        )
        
        # If the item is not created, update the quantity instead
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Redirect to the cart page after adding the item to the cart
        return redirect('cart')



@login_required(login_url='Login')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


from django.shortcuts import redirect, get_object_or_404
from .models import CartItem, Book

@login_required(login_url='Login')
def update_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        quantity_change = int(request.POST.get('quantity_change'))
        if cart_item.quantity + quantity_change > 0:  # Ensure quantity is always positive
            cart_item.quantity += quantity_change
            cart_item.subtotal = cart_item.book.price * cart_item.quantity
            cart_item.total_amount = cart_item.subtotal + cart_item.delivery_charge
            cart_item.save()
            
            # Update stock quantity
            book = cart_item.book
            book.quantity -= quantity_change
            book.save()
    return redirect('cart')

 
from django.shortcuts import render, redirect, get_object_or_404
from .models import BookRequest, Membership
@login_required(login_url='Login')
def book_request(request, book_id):
    book = get_object_or_404(Book, Book_ID=book_id)
    
    # Check if the user has an active membership
    user_membership = Membership.objects.filter(profile=request.user.profile, status=Membership.ACCEPTED).first()

    if request.method == 'POST':
        # Check if the user has an active membership
        if user_membership:
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            pickup_location = request.POST.get('pickup_location')
            
            # Assuming the seller profile is associated with the book
            seller_profile = book.seller_profile

            # Create BookRequest object
            book_request_obj = BookRequest.objects.create(
                full_name=full_name,
                email=email,
                address=address,
                phone_number=phone_number,
                pickup_location=pickup_location,
                profile=request.user.profile,  # Assuming the profile is associated with the current user
                book=book,
                seller_profile=seller_profile
            )
            return redirect('home')
        else:
            
            return redirect('membership')

    return render(request, 'BookRequest.html', {'book': book})

@login_required(login_url='Login')
def Book_status(request):
    book_requests = BookRequest.objects.all()
    return render(request, 'BookRequest_Status.html', {'book_requests': book_requests})


from sslcommerz_lib import SSLCOMMERZ
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from .models import Order, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required(login_url='Login')
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    subtotal = cart_items.aggregate(total_subtotal=Sum('subtotal'))['total_subtotal']
    shipping_cost = cart_items.aggregate(total_shipping=Sum('delivery_charge'))['total_shipping']
    total_amount = subtotal + shipping_cost if subtotal else 0
    return render(request, 'cart.html', {'cart_items': cart_items, 'subtotal': subtotal, 'shipping_cost': shipping_cost, 'total_amount': total_amount})

def create_order(request, total_amount):
    user = request.user
    fname = request.POST.get("fname")
    lname = request.POST.get("lname")
    address = request.POST.get('address')
    address_line2 = request.POST.get('address_line2')
    city_town = request.POST.get('city_town')
    state = request.POST.get('state')
    postcode_zip = request.POST.get('postcode_zip')
    phone_number = request.POST.get('phone_number')
    order_notes = request.POST.get('order_notes')
    payment_status = 'pending'

    if all([fname, lname, address, city_town, state, postcode_zip, phone_number]):
        # Create the order object
        order = Order.objects.create(
            user=user,
            fname=fname,
            lname=lname,
            address=address,
            address_line2=address_line2,
            city_town=city_town,
            state=state,
            postcode_zip=postcode_zip,
            phone_number=phone_number,
            order_notes=order_notes,
            payment_status=payment_status,
            total_amount=total_amount
        )
        return order
    else:
        return None

 

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import Order, OrderItem, Cart
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required(login_url='login')
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    
    user_cart = Cart.objects.filter(user=request.user).first()

    if not user_cart or not user_cart.cartitem_set.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('home')

    cart_items = user_cart.cartitem_set.all()
    subtotal = sum(item.subtotal for item in cart_items)
    shipping = cart_items.aggregate(total_shipping=Sum('delivery_charge'))['total_shipping'] - 100 if cart_items else 0
    total = subtotal + shipping

    if request.method == 'POST':
        payment_option = request.POST.get('payment_option')

        if payment_option == 'sslcommerz_payment':
            sslcz = SSLCOMMERZ({
                'store_id': 'niyam6412dc52e1e89',
                'store_pass': 'niyam6412dc52e1e89@ssl',
                'issandbox': True
            })

            data = {
                'total_amount': str(total),  # Ensure the value is a string
                'currency': 'BDT',
                'tran_id': 'tran_12345',
                'success_url': 'http://127.0.0.1:8000/payment/success/',
                'fail_url': 'http://127.0.0.1:8000/payment/fail/',
                'cancel_url': 'http://127.0.0.1:8000/payment/cancel/',
                'emi_option': '0',
                'cus_name': 'test',
                'cus_email': 'test@test.com',
                'cus_phone': '01700000000',
                'cus_add1': 'customer address',
                'cus_city': 'Dhaka',
                'cus_country': 'Bangladesh',
                'shipping_method': 'NO',
                'multi_card_name': '',
                'num_of_item': 1,
                'product_name': 'Test',
                'product_category': 'Test Category',
                'product_profile': 'general',
            }

            response = sslcz.createSession(data)
            return redirect(response['GatewayPageURL'])
        
        elif payment_option == 'cash_on_delivery':
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            address = request.POST.get('address')
            address_line2 = request.POST.get('address_line2')
            city_town = request.POST.get('city_town')
            state = request.POST.get('state')
            postcode_zip = request.POST.get('postcode_zip')
            phone_number = request.POST.get('phone_number')
            order_notes = request.POST.get('order_notes')
            payment_status = 'pending'

            if all([fname, lname, address, city_town, state, postcode_zip, phone_number]):
                # Create the order object
                order = Order.objects.create(
                    user=request.user,
                    fname=fname,
                    lname=lname,
                    address=address,
                    address_line2=address_line2,
                    city_town=city_town,
                    state=state,
                    postcode_zip=postcode_zip,
                    phone_number=phone_number,
                    order_notes=order_notes,
                    payment_status=payment_status,
                    total_amount=total,
                    order_date=timezone.now()  # Add the order date
                )

                # Once the order is created, create OrderItem instances
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        book=item.book,
                        quantity=item.quantity,
                        price=item.book.price,
                        subtotal=item.subtotal
                    )

                # Remove cart items after successfully creating the order
                user_cart.cartitem_set.all().delete()
                
                messages.success(request, 'Cash on Delivery selected. Your order has been placed.')
                return redirect('cart')
            else:
                messages.error(request, 'Some required fields are missing.')
                return redirect('cart')

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }

    return render(request, 'checkout.html', context)

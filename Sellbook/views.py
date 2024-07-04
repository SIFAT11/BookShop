from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,reverse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from Eshop.models import Book, Category, Membership
from .models import Profile
import random
import string
from .models import Seller_Profile
 
# Create your views here.
 
 
from django.shortcuts import render
 

def home(request):
    category_id = request.GET.get('category_id')
    search_query = request.GET.get('q')  # Get the search query from the request
    location_query = request.GET.get('location')  # Get the location query from the request
    
    books = Book.objects.all()
    
    if category_id:
        try:
            category = Category.objects.get(category_ID=category_id)
            books = books.filter(categories=category)
        except Category.DoesNotExist:
            books = Book.objects.none()
            
    if search_query:
        books = books.filter(title__icontains=search_query)
        
    if location_query:
        books = books.filter(location__icontains=location_query)
        
    # Fetch all categories
    categories = Category.objects.all()
    
    return render(request, 'home.html', {'books': books, 'categories': categories})



def category_books(request, category_id):
    # Fetch the selected category
    category = Category.objects.get(pk=category_id)
    
    # Fetch all books associated with the selected category
    books = Book.objects.filter(categories=category)
    categories = Category.objects.all()
    
    return render(request, 'CategoryBook.html', {'category': category, 'books': books})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

  

@login_required(login_url='Login')
def profile(request):
    # Get the current user's profile
    profile = get_object_or_404(Profile, user=request.user)
    
    try:
        # Try to get the membership associated with the profile
        membership = Membership.objects.get(profile=profile)
    except Membership.DoesNotExist:
        # If membership doesn't exist, set membership to None
        membership = None
    
    context = {
        'profile': profile,
        'membership': membership
    }
    return render(request, 'profile.html', context)

@login_required(login_url='Login')
def membership_view(request):
    membership_requested = Membership.objects.filter(profile=request.user.profile, status__in=[Membership.PENDING, Membership.ACCEPTED]).exists()

    if request.method == 'POST':
        # Assuming you have a form for selecting the membership plan
        plan = request.POST.get('plan')  # Assuming you have a form field named 'plan'
        status = Membership.PENDING  # Assuming the default status is 'Pending'
        
        # Create a new Membership instance
        membership = Membership.objects.create(plan=plan, status=status, profile=request.user.profile)
        
        # Redirect to a success page or payment page
        return redirect('profile') 
    
    # Render the membership form only if the user doesn't have an active membership
    return render(request, 'membership.html', {'membership_requested': membership_requested})



def SellBook_option(request):
    return render(request, 'SellBook.html')


 

def seller_registration(request):
    if request.method == 'POST':
        # Process form submission
        seller_username = request.POST.get('Sellerusername')
        shop_name = request.POST.get('Shop_name')
        address = request.POST.get('address')
        city_town = request.POST.get('city_town')
        postcode_zip = request.POST.get('postcode_zip')
        phone_number = request.POST.get('phone_number')
        age = request.POST.get('age')
        email = request.POST.get('Gmail')
        profile_picture = request.FILES.get('Seller_Profile')
        nid_picture = request.FILES.get('Seller_NID')
        additional_information = request.POST.get('additional_information')
        password = request.POST.get('password')
        re_password = request.POST.get('password1')

        # Validate form data
        if not all([seller_username, shop_name, address, city_town, postcode_zip, phone_number, age, email, password, re_password]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'seller_registration.html', {'data': request.POST})

        if password != re_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'seller_registration.html', {'data': request.POST})

        # Check if the username already exists
        if User.objects.filter(username=seller_username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'seller_registration.html', {'data': request.POST})

        # Create User object
        user = User.objects.create_user(username=seller_username, email=email)
        user.set_password(password)  # Set password
        user.save()
        
        # Create Seller_Profile object
        new_seller = Seller_Profile.objects.create(
            Sellerusername=user,
            Shop_name=shop_name,
            address=address,
            city_town=city_town,
            postcode_zip=postcode_zip,
            phone_number=phone_number,
            age=age,
            Gmail=email,
            Seller_Profile=profile_picture,
            Seller_NID=nid_picture,
            additional_information=additional_information
        )
        # Set request_status to Pending (assuming initial status is Pending)
        new_seller.request_status = Seller_Profile.PENDING
        new_seller.save()

        messages.success(request, 'Your seller request has been submitted. Please wait for approval.')

        # Redirect to home page after successful registration
        return redirect('home')  # Change 'home' to the appropriate URL name
    else:
        return render(request, 'seller_registration.html')


def seller_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # Check if the user is a seller
            if Seller_Profile.objects.filter(Sellerusername=user, request_status=Seller_Profile.ACCEPTED).exists():
                # If the seller's request has been accepted, allow login
                auth.login(request, user)
                return redirect('home')
            else:
                # If the seller's request is not accepted, show error message
                messages.error(request, 'Your request is pending or has been rejected.')
                return redirect('seller_login')
        else:
            # If authentication fails, show error message
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('seller_login')

    return render(request, 'seller_login.html')


 

 
@login_required(login_url='Login')
def seller_profile(request):
    # Check if the user is authenticated and a seller
    if request.user.is_authenticated and hasattr(request.user, 'seller_profile'):
        seller_profile = request.user.seller_profile
        # Retrieve books associated with the seller's profile
        seller_books = seller_profile.book_set.all()  
        context = {
            'seller_profile': seller_profile,
            'seller_books': seller_books  
        }
        return render(request, 'sellerprofile.html', context)
    else:
        return redirect('seller_login')  # Redirect to login page if not authenticated or not a seller



def Booklist(request):
    search_query = request.GET.get('q', '')
    books = Book.objects.all().order_by('-upload_date')  # Ensure the books are sorted by upload date
    if search_query:
        books = books.filter(title__icontains=search_query)
    return render(request, 'BookList.html', {'books': books})
from enum import auto
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from Sellbook.models import Profile
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login  # Rename the login function
from django.contrib.auth import login
from Sellbook.models import Seller_Profile 
 


def register_profile(request):
    if request.method == 'POST':
        # Extracting form data
        name = request.POST['name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        address_line2 = request.POST['address_line2']
        city_town = request.POST['city_town']
        postcode_zip = request.POST['postcode_zip']
        phone_number = request.POST['phone_number']
        age = request.POST['age']
        gender = request.POST['gender']
        nid_number = request.POST.get('nid_number')
        email = request.POST['email']
        profile_picture = request.FILES.get('profile_picture')
        password = request.POST['password']
        password1 = request.POST['password1']
        additional_information = request.POST['additional_information']

        # Validate password length and match
        if password != password1:
            messages.error(request, 'Passwords do not match.')
            return redirect('Registreation')

        elif not 8 <= len(password) <= 10:
            messages.error(request, 'Password should be 8-10 characters long. Please insert a valid password.')
            return redirect('Registreation')

        # Check if username or email already exists
        if User.objects.filter(username=name).exists():
            messages.error(request, 'Username already exists. Please use another name.')
            return redirect('Registreation')

        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email address is already taken. Please use another email address.')
            return redirect('Registreation')

        # Create user and profile if all checks pass
        user = User.objects.create_user(username=name, first_name=first_name, last_name=last_name,
                                        email=email, password=password)
        profile = Profile.objects.create(user=user, address=address, address_line2=address_line2,
                                          city_town=city_town,
                                          postcode_zip=postcode_zip, phone_number=phone_number, age=age,
                                          gender=gender,
                                          nid_number=nid_number,
                                          additional_information=additional_information,
                                          profile_picture=profile_picture)  # Assign profile picture
        messages.success(request, 'Your registration is successful. Please login.')
        return redirect('Login')

    return render(request, 'register_profile.html')

 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Change 'name' to 'username'
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            # Check if the user is a seller
            if Seller_Profile.objects.filter(Sellerusername=user).exists():
                # If the user is a seller, show error message and redirect
                messages.error(request, 'Sellers cannot log in here. Please use the seller login page.')
                return redirect('seller_login')  # Redirect to the seller login page
            else:
                # If the user is not a seller, proceed with the standard login process
                login(request, user)
                return redirect('home')
        else:
            # If authentication fails, show error message
            messages.error(request, 'Username or password incorrect.')
            return redirect('Login')  # Redirect back to the login page

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('Login')
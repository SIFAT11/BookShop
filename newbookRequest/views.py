from django.shortcuts import render, redirect
from .models import newbookRequest as NewBookRequestModel
from django.contrib.auth.decorators import login_required

@login_required(login_url='seller_login')
def newbookRequest(request):
    if request.method == 'POST':
        # Retrieve data from the form
        book_name = request.POST.get('book_name')
        writter_name = request.POST.get('writter_name')
        publication = request.POST.get('publication')
        edition = request.POST.get('edition')
        phone_number = request.POST.get('phone_number')  # Added phone number field
        email = request.POST.get('email')  # Added email field
        book_image = request.FILES.get('book_image')

        # Create a new book request object
        new_request = NewBookRequestModel.objects.create(
            book_name=book_name,
            writter_name=writter_name,  # Corrected to lowercase
            publication=publication,
            edition=edition,
            phone_number=phone_number,
            email=email,
            book_image=book_image
        )

        # Redirect to a success page or homepage
        return redirect('newbookRequest')  # You can replace 'success_page' with the URL name of your success page

    # If the request method is GET, render the form
    return render(request, 'newbookRequest.html')

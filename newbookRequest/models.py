from django.db import models

class newbookRequest(models.Model):
    book_name = models.CharField(max_length=100)
    writter_name = models.CharField(max_length=100)  # Changed Writter_name to writter_name for consistency
    publication = models.CharField(max_length=100)
    edition = models.CharField(max_length=100)
    book_image = models.ImageField(upload_to='book_images/', default='None')
    request_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15)  # Added phone number field
    email = models.EmailField()  # Added email field

    def __str__(self):
        return self.book_name

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Book
from datetime import datetime

# Read all books
def get_books(request):
    books = list(Book.objects.values())
    return JsonResponse(books, safe=False)

# Read single book
def get_book(request, id):
    try:
        book = Book.objects.get(pk=id)
        return JsonResponse({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "published_date": book.published_date
        })
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

@csrf_exempt
def create_book(request):
    if request.method == "GET":
        # Show a simple HTML form
        return HttpResponse('''
            <h2>Create Book (via API)</h2>
            <form method="POST">
                Title: <input type="text" name="title"><br><br>
                Author: <input type="text" name="author"><br><br>
                Published Date: <input type="date" name="published_date"><br><br>
                <input type="submit" value="Create Book">
            </form>
        ''')
    
    if request.method == "POST":
        # This will handle data from a browser form (not JSON)
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')

        if not (title and author and published_date):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        book = Book.objects.create(
            title=title,
            author=author,
            published_date=published_date
        )
        return JsonResponse({'message': 'Book created', 'id': book.id})
    
    return JsonResponse({'error': 'Invalid method'}, status=405)

# Update book
@csrf_exempt
def update_book(request, id):
    book = get_object_or_404(Book, pk=id)

    if request.method == "GET":
        # Show a basic HTML form to update the book
        return HttpResponse(f'''
            <h2>Update Book (ID: {book.id})</h2>
            <form method="POST">
                Title: <input type="text" name="title" value="{book.title}"><br><br>
                Author: <input type="text" name="author" value="{book.author}"><br><br>
                Published Date: <input type="date" name="published_date" value="{book.published_date}"><br><br>
                <input type="submit" value="Update Book">
            </form>
        ''')

    elif request.method == "POST":
        # Get form data
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')

        if not (title and author and published_date):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        # Update the book
        book.title = title
        book.author = author
        book.published_date = published_date
        book.save()

        return JsonResponse({'message': f"Book '{book.title}' updated successfully", 'id': book.id})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Delete book
@csrf_exempt
def delete_book(request, id):
    book = get_object_or_404(Book, pk=id)

    if request.method == "GET":
        # Show a confirmation form
        return HttpResponse(f'''
            <h2>Are you sure you want to delete: <b>{book.title}</b>?</h2>
            <form method="POST">
                <input type="submit" value="Yes, Delete">
            </form>
            <br>
            <a href="/api/books/">Cancel</a>
        ''')

    elif request.method == "POST":
        book.delete()
        return HttpResponse(f"Book '{book.title}' deleted successfully!")

    return JsonResponse({'error': 'Method not allowed'}, status=405)

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import render
from django.views import generic

from catalog.models import Author, Book, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # The 'all()' method is implied by default
    num_authors = Author.objects.count()

    # Total genres
    num_genres = Genre.objects.count()

    # Books containing the word 'game'
    num_game_books = Book.objects.filter(title__icontains='game').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_game_books': num_game_books,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorList(generic.ListView):
    model = Author
    paginate_by = 5


class AuthorDetail(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksList(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan by all users."""
    model = BookInstance
    template_name = 'catalog/bookinstance_all_borrowed.html'
    paginate_by = 10
    permission_required = ('catalog.can_mark_returned', )

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

from django.contrib import admin

from catalog.models import Author, Book, BookInstance, Genre, Language


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(Language)

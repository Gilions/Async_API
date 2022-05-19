from django.contrib import admin
from django.db.models import Prefetch

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmWork


class GenreFilmworkInline(admin.StackedInline):
    model = GenreFilmwork
    autocomplete_fields = ['genre', 'film_work']
    list_prefetch_related = (Prefetch('film_work'), Prefetch('genre'))

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            *self.list_prefetch_related
        )


class PersonFilmWorkAdmin(admin.StackedInline):
    model = PersonFilmWork
    autocomplete_fields = ['person', 'film_work']
    list_prefetch_related = (Prefetch('film_work'), Prefetch('person'))

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            *self.list_prefetch_related
        )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', )
    search_fields = ('id', 'name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):

    list_display = ('full_name', )
    search_fields = ('id', 'full_name', )


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_prefetch_related = (Prefetch('persons'), Prefetch('genres'), )
    inlines = (GenreFilmworkInline, PersonFilmWorkAdmin, )

    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request).prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres',)

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'

    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')

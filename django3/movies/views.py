from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ReviewForm
from .models import Actor, Category, Genre, Movie


class GenreYear:
    '''Жанры и годы выхода фильмов'''

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(is_draft=False).order_by('year')


class MoviesListView(GenreYear, ListView):
    '''Список фильмов'''
    model = Movie
    queryset = Movie.objects.filter(is_draft=False)


class MovieDetailView(GenreYear, DetailView):
    '''Полное описание фильма'''
    model = Movie
    slug_field = 'url'


class AddReview(View):
    '''Оставить отзыв'''
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        if form.is_valid():
            # приостановка сохранения формы
            form = form.save(commit=False)
            if request.POST.get('parent'):
                # parent_id in DB
                form.parent_id = int(request.POST.get('parent'))
            movie = Movie.objects.get(pk=pk)
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorDetailView(GenreYear, DetailView):
    '''Информация об актёре / режиссёре'''
    model = Actor
    # template_name = 'movies/actor_detail.html'
    slug_field = 'name'


class MoviesFilterView(GenreYear, ListView):
    '''Фильтрация фильмов'''

    def get_queryset(self):
        return Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        )


class JSONFilterMoviesView(ListView):
    '''Фильтрация фильмов в json'''

    def get_queryset(self):
        return Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct().values('title', 'tagline', 'url', 'poster')
    
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {'movies': list(self.get_queryset())},
            safe=False,
        )
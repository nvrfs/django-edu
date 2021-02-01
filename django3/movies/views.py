from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .models import Movie


class MoviesListView(ListView):
    '''Список фильмов'''
    model = Movie
    queryset = Movie.objects.filter(is_draft=False)


class MovieDetailView(DetailView):
    '''Полное описание фильма'''
    model = Movie
    slug_field = 'url'


class AddReview(View):
    '''Оставить отзыв'''
    def post(self, request, pk):
        print(request.POST)
        return redirect('/')
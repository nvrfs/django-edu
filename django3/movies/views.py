from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ReviewForm
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

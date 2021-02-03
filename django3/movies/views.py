from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import RatingForm, ReviewForm
from .models import Actor, Category, Genre, Movie, Rating


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
    paginate_by = 3


class MovieDetailView(GenreYear, DetailView):
    '''Полное описание фильма'''
    model = Movie
    slug_field = 'url'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['star_form'] = RatingForm()
        return context


class AddReviewView(View):
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


class AddRatingView(View):
    '''Добавить рейтинг'''
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forrwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))},
            )
            return HttpResponse(status=201)
        return HttpResponse(statis=400)


class ActorDetailView(GenreYear, DetailView):
    '''Информация об актёре / режиссёре'''
    model = Actor
    # template_name = 'movies/actor_detail.html'
    slug_field = 'name'


class MoviesFilteredView(GenreYear, ListView):
    '''Фильтрация фильмов'''

    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join(
            [f'year={x}&' for x in self.request.GET.getlist('year')]
        )
        context['genre'] = ''.join(
            [f'genre={x}&' for x in self.request.GET.getlist('genre')]
        )
        return context



class MoviesJSONFilteredView(ListView):
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
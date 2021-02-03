from django.urls import path

from .views import (
    ActorDetailView,
    AddRatingView,
    AddReviewView,
    JSONFilterMoviesView,
    MoviesFilterView,
    MovieDetailView,
    MoviesListView
)

urlpatterns = [
    path('', MoviesListView.as_view(), name='movies_list'),
    path('rating/', AddRatingView.as_view(), name='add_rating'),
    path('filter/', MoviesFilterView.as_view(), name='movies_filter'),
    path('json-filter/', JSONFilterMoviesView.as_view(), name='json_filter'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', AddReviewView.as_view(), name='add_review'),
    path('actor/<str:slug>/', ActorDetailView.as_view(), name='actor_detail'),
]

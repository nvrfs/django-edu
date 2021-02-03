from modeltranslation.translator import register, TranslationOptions
from .models import Actor, Category, Genre, Movie, MovieShot


@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country')


@register(MovieShot)
class MovieShotTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

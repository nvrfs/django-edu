from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    '''Категория'''
    name = models.CharField('Категория', max_length=128)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    '''Актёр / режиссёр'''
    name = models.CharField('ФИО', max_length=64)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актёр / режиссёр'
        verbose_name_plural = 'Актёры / режиссёры'


class Genre(models.Model):
    '''Жанр'''
    name = models.CharField('Название', max_length=64)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    '''Фильм'''
    title = models.CharField('Название', max_length=128)
    tagline = models.CharField('Слоган', max_length=256, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Год выхода', default=1895)
    country = models.CharField('Страна', max_length=64)
    directors = models.ManyToManyField(
        Actor, verbose_name='Режиссёр', related_name='movie_director'
    )
    actors = models.ManyToManyField(
        Actor, verbose_name='Актёр', related_name='movie_actor'
    )
    genres = models.ManyToManyField(Genre, verbose_name='Жанр')
    world_premiere = models.DateField(
        'Дата премьеры в мире', default=date.today
    )
    budget = models.PositiveIntegerField(
        'Бюджет', default=0, help_text='указывать сумму в долларах'
    )
    usa_fees = models.PositiveIntegerField(
        'Сборы в США', default=0, help_text='указывать сумму в долларах'
    )
    worldwide_fees = models.PositiveIntegerField(
        'Сборы в мире', default=0, help_text='указывать сумму в долларах'
    )
    category = models.ForeignKey(Category, verbose_name='Категория',
        on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=128, unique=True)
    is_draft = models.BooleanField('Черновик', default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_reviews(self):
        return self.review_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShot(models.Model):
    '''Кадр из фильма'''
    title = models.CharField('Заголовок', max_length=128)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class RatingStar(models.Model):
    '''Звёзды рейтинга'''
    value = models.SmallIntegerField('', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звёзды рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'


class Rating(models.Model):
    '''Рейтинг'''
    ip = models.CharField('IP-адрес', max_length=16)
    star = models.ForeignKey(
        RatingStar, verbose_name='Звёзды', on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.star} - {self.movie}'
    
    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    '''Отзыв'''
    email = models.EmailField()
    name = models.CharField('Имя', max_length=64)
    text = models.TextField('Текст', max_length=2048)
    parent = models.ForeignKey('self', verbose_name='Ответ к',
        on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} - {self.movie}'
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Category, Genre, Movie, MovieShot, Actor, Rating, RatingStar, Review
)

admin.site.site_title = 'Movies'
admin.site.site_header = 'Movies'


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(
        label='Описание', widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = Movie
        fields = '__all__'


class MovieShotInline(admin.TabularInline):
    model = MovieShot
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50">')
    
    get_image.short_description = 'Изображение'


class ReviewInline(admin.TabularInline):  # +StackedInline
    model = Review
    extra = 1
    readonly_fields = ('name', 'email')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'year', 'url', 'is_draft')
    list_display_links = ('pk', 'title')
    list_filter = ('category', 'year')
    list_editable = ('is_draft',)
    fields = (
        ('title', 'tagline'),
        ('description', 'poster', 'get_image'),
        ('year', 'world_premiere', 'country'),
        ('actors', 'directors', 'genres', 'category'),
        ('budget', 'usa_fees', 'worldwide_fees'),
        ('url', 'is_draft'),
    )
    readonly_fields = ('get_image',)
    search_fields = ('title', 'category__name')
    inlines = [MovieShotInline, ReviewInline]
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    save_on_top = True
    save_as = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50">')

    def publish(self, request, queryset):
        row_update = queryset.update(is_draft=False)
        self.message_user(request, f'записей обновлено: {row_update}')

    def unpublish(self, request, queryset):
        row_update = queryset.update(is_draft=True)
        self.message_user(request, f'записей обновлено: {row_update}')

    get_image.short_description = 'Постер'

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'parent', 'movie')
    list_display_links = ('pk', 'name')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(MovieShot)
class MovieShotAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50">')
    
    get_image.short_description = 'Изображение'


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50">')
    
    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'movie', 'star', 'ip')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'url')
    list_display_links = ('pk', 'name')

admin.site.register(RatingStar)

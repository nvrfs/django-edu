from django import forms

from .models import Rating, RatingStar, Review


class ReviewForm(forms.ModelForm):
    '''Форма отзывов'''

    class Meta:
        model = Review
        fields = ('name', 'email', 'text')


class RatingForm(forms.ModelForm):
    '''Форма рейтинга'''

    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(),
        widget=forms.RadioSelect(),
        empty_label=None,
    )

    class Meta:
        model = Rating
        fields = ('star',)

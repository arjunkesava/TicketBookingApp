from django import forms
from django.forms import ModelForm
from Book.models import SeatingTable, MovieActiveDays, ActiveShowTimings

class SeatingForm(forms.ModelForm):
    class Meta:
        model = SeatingTable
        widgets = {
            'seatlayouttext': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = '__all__'

class MovieActiveDaysForm(ModelForm):
    from_date_field = forms.DateField()
    end_date_field = forms.DateField()
    class Meta:
        model = MovieActiveDays
        fields = ['moviedetails', 'theaterbase']

class ActiveShowTimingsForm(ModelForm):
    from_date_field = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    end_date_field = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = MovieActiveDays
        fields = ['moviedetails', 'theaterbase']
        widgets = {
            'moviedetails': forms.Select(attrs={'class': 'form-control'}),
            'theaterbase': forms.Select(attrs={'class': 'form-control'}),
        }

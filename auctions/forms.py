from django.forms import ModelForm, HiddenInput
from .models import Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startingPrice', 'imageLink', 'category']

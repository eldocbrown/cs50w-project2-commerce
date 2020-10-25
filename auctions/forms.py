from django.forms import ModelForm, HiddenInput
from .models import Listing, Bid, Comment
from django.forms.widgets import TextInput, Textarea, NumberInput, URLInput

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'imageLink', 'category', 'startingPrice']
        labels = {"title": "", "description": "", "imageLink": "", "startingPrice": ""}
        widgets = {
            'title': TextInput(attrs={  'placeholder': 'Title',
                                        'id': 'listingFormTitle'}),
            'description': Textarea(attrs={ 'placeholder': 'Type the auction description here',
                                            'id': 'listingFormDescription'}),
            'imageLink': URLInput(attrs={   'placeholder': 'Image URL Link',
                                            'id': 'listingFormImageLink'}),
            'startingPrice': NumberInput(attrs={'placeholder': 'Starting Price',
                                                'id': 'listingFormStartingPrice'}),
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        labels = {"price": "Bid"}

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

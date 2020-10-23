from django.forms import ModelForm, HiddenInput
from .models import Listing, Bid, Comment

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startingPrice', 'imageLink', 'category']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        labels = {"price": "Bid"}

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

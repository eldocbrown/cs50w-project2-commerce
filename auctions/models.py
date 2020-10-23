from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    listingsWatched = models.ManyToManyField('Listing', blank=True, related_name="watchedBy")

class Category(models.Model):
    name = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usrBids")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="listingBids")
    created_at = models.DateTimeField(auto_now_add=True)

class Listing(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    startingPrice = models.DecimalField(max_digits=10, decimal_places=2)
    imageLink = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="catListings", null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usrListings")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lastBid = models.ForeignKey(Bid, on_delete=models.SET_NULL, null=True, blank=True, related_name="bidListing")

    def bid(self, bid):
        if self.lastBid is None:
            if bid.price >= self.startingPrice:
                self.lastBid = Bid(bid)
            else:
                raise ValueError
        else:
            if bid.price > self.lastBid.price:
                self.lastBid = Bid(bid)
            else:
                raise ValueError

    def price(self):
        if self.lastBid is not None:
            return self.lastBid.price
        else:
            return self.startingPrice

class Comment(models.Model):
    comment = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usrComments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingComments")
    created_at = models.DateTimeField(auto_now_add=True)

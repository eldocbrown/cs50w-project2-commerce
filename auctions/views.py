from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Category
from .forms import ListingForm, BidForm, CommentForm

def index(request):
    listings = Listing.objects.filter(active=True)
    return renderListing(request, listings, "Active listings")

def categories(request):
    categories = Category.objects.all().order_by('name')
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def categoryListing(request, id):
    category = Category.objects.get(pk=id)
    listings = Listing.objects.filter(category=category, active=True)
    return renderListing(request, listings, f"{category.name} active listings")

@login_required(login_url="auctions:login")
def watchlist(request):
    listings = User.objects.get(username=request.user.username).listingsWatched.all()
    return renderListing(request, listings, "Watchlist")

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="auctions:login")
def create(request):
    if request.method == "POST":
        f = ListingForm(request.POST)
        if f.is_valid():
            new_listing = f.save(commit=False)
            new_listing.creator = request.user
            new_listing.save()
            f.save_m2m()
            # TODO: Go to listing page after creating
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return renderError(request, f.errors)
    else:
        return render(request, "auctions/create.html", {
            "createListingForm": ListingForm()
        })

def listing(request, id):
    l = getListing(id)
    return render(request, "auctions/listing.html", {
        "listing": l,
        "bidForm": BidForm(),
        "watchers": l.watchedBy.all(),
        "commentForm": CommentForm(),
        "comments": l.listingComments.all().order_by('-created_at'),
        "bidCount": getBidCount(id)
    })

@login_required(login_url="auctions:login")
def bid(request, id):
    l = getListing(id)
    f = BidForm(request.POST)
    if f.is_valid():
        # Get Bid object
        bid = f.save(commit=False)
        # Set bidder and relate to listing
        bid.bidder = request.user
        bid.listing = l
        try: # Try setting bid to listing
            l.bid(bid)
        except Exception as ex:
            return renderError(request, "Invalid Bid")
        else:
            # Save data
            bid.save()
            l.save()
            f.save_m2m()
            # Redirect to the listing page again
            return redirectToListing(id)
    else:
        return renderError(request, "Invalid Bid")

@login_required(login_url="auctions:login")
def addwatch(request, id):
    l = getListing(id)
    try:
        u = User.objects.get(username=request.user.username)
        u.listingsWatched.add(l)
        return redirectToListing(id)
    except Exception as e:
        return renderError(request, e)

@login_required(login_url="auctions:login")
def removewatch(request, id):
    l = getListing(id)
    try:
        u = User.objects.get(username=request.user.username)
        u.listingsWatched.remove(l)
        return redirectToListing(id)
    except Exception as e:
        return renderError(request, e)
    return redirectToListing(id)

@login_required(login_url="auctions:login")
def close(request, id):
    l = getListing(id)
    try:
        l.active = False
        l.save()
    except Exception as e:
        return renderError(request, e)
    else:
        return redirectToListing(id)

@login_required(login_url="auctions:login")
def comment(request, id):
    l = getListing(id)
    f = CommentForm(request.POST)
    if f.is_valid():
        # Get Comment object
        comm = f.save(commit=False)
        # Set commenter and relate to listing
        comm.commenter = request.user
        comm.listing = l
        # Save data
        comm.save()
        f.save_m2m()
        # Redirect to the listing page again
        return redirectToListing(id)
    else:
        return renderError(request, "Invalid comment")

# Auxiliary functions
def getListing(id):
    try:
        return Listing.objects.get(pk=id)
    except ObjectDoesNotExist:
        return renderError(request, "Listing not found.")
    except Exception as e:
        return renderError(request, e)

def getBidCount(id):
    try:
        return Listing.objects.get(pk=id).listingBids.count()
    except ObjectDoesNotExist:
        return renderError(request, "Listing not found.")
    except Exception as e:
        return renderError(request, e)

def renderError(request, message):
    return render(request, "auctions/error.html", {
        "message": message
    })

def redirectToListing(id):
    return HttpResponseRedirect(reverse("auctions:listing", kwargs={'id':id}))

def renderListing(request, listings, heading):
    return render(request, "auctions/index.html", {
        "listings": listings,
        "heading": heading
    })

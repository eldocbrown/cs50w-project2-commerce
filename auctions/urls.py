from django.urls import path

from . import views


app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("listing/<str:id>/bid", views.bid, name="bid"),
    path("listing/<str:id>/addwatch", views.addwatch, name="addwatch"),
    path("listing/<str:id>/removewatch", views.removewatch, name="removewatch"),
    path("listing/<str:id>/close", views.close, name="close"),
    path("listing/<str:id>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
]

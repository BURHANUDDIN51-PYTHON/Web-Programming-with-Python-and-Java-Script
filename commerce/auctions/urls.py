from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create',views.create_listing, name="create"),
    path('<int:listing_id>', views.listing, name="listing"),
    path('<int:listing_id>/watchlist/<str:add_remove>', views.watchlist, name='watchlist'),
    path('displaywatchlist',views.display_watchlist, name="displaywatchlist"),
    path('comment', views.add_comment, name="comment"),
    path('close/<int:listing_id>', views.close_bidding, name="close")
]

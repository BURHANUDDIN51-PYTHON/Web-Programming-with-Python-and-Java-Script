from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listings, Category, Bid, Comments
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == "GET":
        active_list = Listings.objects.filter(is_active=True).all()
        return render(request, "auctions/index.html", {
            "listings":active_list,
            "category": Category.objects.all()
            })
    else:
        category = Category.objects.filter(pk=request.POST['category']).first()
        return render(request, "auctions/index.html", {
            "listings": category.categories.all(),
            "category": Category.objects.all(),
            })
        


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def create_listing(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_bid = request.POST.get('bid')
        url = request.POST.get('url')
        category = request.POST.get('category')
        cat = Category.objects.filter(id=category).first()
        current_user = request.user
        list = Listings(title=title,description=description,starting_bid=float(starting_bid),url=url,category=cat,owner=current_user)
        list.save()
        bid_for = Bid(bid=starting_bid, listing=list, bidder=current_user)
        bid_for.save()
        return render(request, 'auctions/create.html', {
            "message":"Listing Created successfully",
            "category": Category.objects.all()}
        )
    else:
        return render(request, "auctions/create.html", {"category": Category.objects.all()})
    

def listing(request, listing_id):
    is_watchlist = False
    current_user = request.user
    listing = Listings.objects.filter(pk=listing_id).first()
    bids_on_listing = listing.bids.all()
    if current_user in listing.watchlist.all():
        is_watchlist = True
    max_bid = 0
    for each_bid in bids_on_listing:
        if each_bid.bid >= max_bid:
            max_bid = each_bid.bid
    
    highest_bidder = Bid.objects.filter(bid=max_bid).filter(listing=listing).first()
    
    is_owner = False      
    if listing.owner == current_user:
        is_owner = True
            
    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "list": Listings.objects.filter(id=listing_id).first(),
            "is_watchlist":is_watchlist,
            "max": max_bid,
            "comments":listing.comments.all(),
            "is_owner" : is_owner,
            "bidder": f'The Bid has been close and the winner is {highest_bidder.bidder}',
            })
    else:
        bid = request.POST['bid']
        if float(bid) <= max_bid:
            return render(request, "auctions/listing.html", {
                "list": Listings.objects.filter(id=listing_id).first(),
                "is_watchlist":is_watchlist,
                'max':max_bid,
                "message":f"The bid must be larger than the existing Bid",
                'comments': listing.comments.all()
            })
        another_bid = Bid(bid=float(bid),listing=listing,bidder=current_user)
        another_bid.save()
        return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
        



def watchlist(request, listing_id, add_remove):
    if request.method == "POST":
        # If false mean to add to watch list if true remove from watchlist
        add_remove = True if add_remove == 'True' else False
        listing = Listings.objects.filter(pk=listing_id).first()
        current_user = request.user
        if add_remove == False:
            listing.watchlist.add(current_user)
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
        else:
            listing.watchlist.remove(current_user)
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
        
        
@login_required
def display_watchlist(request):
    current_user = request.user
    watchlist_listing = current_user.users_watchlist.all()
    return render(request, "auctions/watchlist.html", {
        'listings': watchlist_listing
    })
            

@login_required
def add_comment(request):
    if request.method == "POST":
        current_user = request.user
        comment = request.POST['comment']
        listing = Listings.objects.filter(pk=request.POST['id']).first()
        add_a_comment = Comments(comment=comment,user=current_user,listing=listing)
        add_a_comment.save()
        return HttpResponseRedirect(reverse('listing', args=(request.POST['id'],)))
    
    
@login_required
def close_bidding(request, listing_id):
    if request.method == "POST":
        max_bid = request.POST['max']
        listing = Listings.objects.filter(pk=listing_id).first()
        listing.is_active = False
        listing.save()
        highest_bidder = Bid.objects.filter(bid=max_bid).filter(listing=listing).first()
        return render(request, "auctions/listing.html", {
            "list": Listings.objects.filter(id=listing_id).first(),
            "max": max_bid,
            "comments":listing.comments.all(),
            "bidder": f'The Bid has been close and the winner is {highest_bidder.bidder}',
            "is_watchlist": False
            })
        
        
        
            
from django.contrib import messages, auth
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Movies, Details, Category
from django.shortcuts import render, redirect
from .forms import MovieForm, DetailsForm, UserProfileForm
from django.contrib.auth.models import User


def home(request):
    movie=Movies.objects.all()
    context={'movie_list':movie}
    return render(request,'home.html',context)



def details(request,movie_id):

    movie1=get_object_or_404(Movies,id=movie_id)
    review=Details.objects.filter(movie_title=movie1)
    return render(request, 'details.html',{'mve': movie1,'rvw':review})


def review(request,movie_id):
    movie1 = get_object_or_404(Movies, id=movie_id)
    review1 = Details.objects.filter(movie_title=movie1)
    if request.method=='POST':
        rtg=request.POST.get('rating')
        revw=request.POST.get('review')
        print(f'Rating: {rtg}, Review: {revw}')
        dtls=Details(review=revw,rating=rtg,movie_title=movie1)
        dtls.save()
        return redirect('moviereviewapp:review',movie_id=movie_id)
    return render(request, 'review.html', {'mve': movie1,'rvw': review1})


def login(request):

    if request.method == 'POST':
        username=request.POST['User_Name']
        password=request.POST['Password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('moviereviewapp:user_login')
        else:
            messages.info(request,"User not registered/Incorrect credentials")
            return redirect('moviereviewapp:login')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        uname = request.POST['User_Name']
        fname = request.POST['First_Name']
        lname = request.POST['Last_Name']
        email = request.POST['Email']
        pwd = request.POST['Password']
        cpwd = request.POST['Password1']
        if pwd==cpwd:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "User Name Exists")
                return redirect('moviereviewapp:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Id already exist")
                return redirect('moviereviewapp:register')
            else:
                user = User.objects.create_user(username=uname,first_name=fname,last_name=lname,email=email,password=pwd,)
                user.save()
                messages.info(request, "Registered Successfully")
        else:
            messages.info(request, "Password Not Matching")
            return redirect('moviereviewapp:register')
        return redirect('/')
    return render(request, 'register.html')


def add_movie(request):
    if request.method=='POST':
        title=request.POST.get('title')
        category_name = request.POST.get('category')
        desc=request.POST.get('desc')
        actors=request.POST.get('actors')
        release_date=request.POST.get('release_date')
        poster=request.FILES['poster']
        utube_link=request.POST.get('utube_link')
        luser=request.user.id

        category = get_object_or_404(Category, name=category_name)

        movie=Movies(title=title,category=category,desc=desc,actors=actors,release_date=release_date,poster=poster,utube_link=utube_link,login_user=luser)
        movie.save()
        return redirect('moviereviewapp:user_login')
    return render(request,'add_movie.html')


def user_login(request):
    dlist=None
    lid=None
    if request.user.is_authenticated:
        context = request.user.first_name
        lid = request.user.id
    else:
        context=None
        dlist = None
    mlist = Movies.objects.all()
    if Details.movie_title == Movies.title:
        dlist = Details.objects.all()
    return render(request, 'user_login.html', {'user':context,'movie_list':mlist,'luser':lid,'detail_list':dlist})


def update(request, id):
    mve = Movies.objects.get(id=id)
    form=MovieForm(request.POST or None,request.FILES,instance=mve)

    if form.is_valid():
        form.save()

        return redirect('moviereviewapp:user_login')
    return render(request,'edit_movies.html',{'form':form,'movie':mve})


def update_profile(request,id):
    user = get_object_or_404(User, id=id)
    form=UserProfileForm(request.POST or None,request.FILES,instance=user)
    if form.is_valid():
        form.save()
        messages.info(request, "Updated Successfully")
        return redirect('moviereviewapp:my_profile',id)

    return render(request, 'update_profile.html',{'id':user,'form':form})


def categorylist(request,c_slug):
    c_page = None
    movie_list = None

    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movie_list = Movies.objects.filter(category=c_page, available=True)
    else:
        movie_list = Movies.objects.filter(available=True)

    paginator = Paginator(movie_list, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        movies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        movies = paginator.page(paginator.num_pages)

    return render(request, "category.html", {'category': c_page, 'movies': movies})


def delete(request, id):
    if request.method=='POST':
        movie1=Movies.objects.get(id=id)
        movie1.delete()
        return redirect('moviereviewapp:user_login')
    return render(request,'delete_movies.html')


def delete_profile(request,id):
    if request.method=='POST':
        user1=User.objects.get(id=id)
        user1.delete()
        return redirect('/')
    return render(request,'delete_profile.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def my_profile(request,id):
    user = get_object_or_404(User, pk=id)
    return render(request,'my_profile.html',{'user':user})


def search(request):
    movies=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        movies=Movies.objects.filter(Q(title__icontains=query) | Q(actors__icontains=query))
    return render(request,'search.html',{'query':query,'movies':movies})



from django.urls import path, include
from . import views

app_name = 'moviereviewapp'

urlpatterns = [
    path('', views.home,name='home'),
    path('movie/<int:movie_id>/', views.details, name='details'),
    path('movie/<int:movie_id>', views.review, name='review'),
    # path('<slug:c_slug>/', views.category, name='category'),
    path('add/', views.add_movie, name='add_movie'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('user_login/',views.user_login,name='user_login'),
    path('update_profile/<int:id>',views.update_profile,name='update_profile'),
    path('update/<int:id>/',views.update,name='update'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('delete_profile/<int:id>/',views.delete_profile,name='delete_profile'),
    path('my_profile/<int:id>',views.my_profile,name='my_profile'),
    path('logout/',views.logout,name='logout'),
    path('search/',views.search,name='search'),
    path('category/<slug:c_slug>', views.categorylist, name='categorylist'),

]
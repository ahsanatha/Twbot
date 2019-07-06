from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('callback/', views.callback, name='callback'),
    path('home/', views.home, name='home'),
    # path('state/', views.state, name='state'),
    path('delAll/', views.delAllTweet, name='delAll'),
    path('logout/',views.logout,name='logout'),
    # path('delX/', views.delXTweet, name='delX'),
]

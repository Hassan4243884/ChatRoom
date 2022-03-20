from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path("login/",views.loginPage,name="login"),
    path("logout/",views.logoutPage,name="logout"),
    path("register/",views.registerUser,name="register"),


    path("",views.home,name="home"),
    path("room/<str:pk>",views.room,name="room"),
    path("profile/<str:pk>",views.userProfile,name="user-profile"),

    path("create_room/",views.createRoom,name="create_room"),
    path("update_room/<str:pk>/",views.updateRoom,name="update_room"),
    path("delete_room/<str:pk>/",views.deleteRoom,name="delete_room"),
    path("delete_message/<str:pk>/",views.deleteMessage,name="delete_message"),
    

    path("update-user/",views.updateUser,name="update-user"),
    path("topic-page/",views.topicPage,name="topic-page"),
    path("activity-page/",views.activityPage,name="activity-page"),

]
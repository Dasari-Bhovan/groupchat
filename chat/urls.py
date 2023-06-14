from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


app_name = "chat"
urlpatterns = [
    path("", views.home, name="home"),
    path("<grp_name>", views.group, name="group"),
    path("profile/<slug:user_name>", views.profile, name="profile"),
    path("group_profile/<slug:grp_name>", views.group_profile, name="group_profile"),
    path("search_user/", views.search_user, name="search_user"),
    path("<grp_name>/add_members", views.add_member, name="add_members"),
    #api urls
    path("api/login",views.LoginView.as_view()),
    path("api/register",views.RegisterView.as_view()),
    path("api/logout",views.logoutView.as_view()),
    path("api/groups",views.GroupView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns,allowed=["json","html"])

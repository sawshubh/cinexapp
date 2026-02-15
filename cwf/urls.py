from django.urls import path, re_path
from . import app_init
from cwf.cnx.webservice import cnx_movies

urlpatterns = [
    path("", app_init.show_homepage),
    path("login/", app_init.show_login_page, name="show_login_page"),
    path("home/", app_init.index, name="index"),
    path("onboard-user/", app_init.onboard_user, name="onboard-user"),
    # cnx webservice
    # path("movie-data-insertion/", cnx_movies.onboard_user, name="movie-data-insertion"),
]

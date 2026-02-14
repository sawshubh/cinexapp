from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from cwf.models import checkpoint, CustomUser
from cwf.utils import get_environment, is_ajax_request


def show_homepage(request):
    if request.get_host().find(":8025") != -1 or request.method == "POST":
        return show_loginpage(request)


def show_loginpage(request):
    login_page = "cwf/login.html"
    if request.get_host().find(":8025") != -1:
        login_page = "cwf/cnx/cnx_login.html"

    template_dict = {
        "env": get_environment(request),
        "is_error": False,
        "is_user_inactive": False,
        "app_config": get_app_config_obj(),
        "selected_lang": "en",
        "social_login_applicable": False,
    }

    if request.method == "POST":
        user = authenticate(
            user_id=request.POST["user_id"],
            password=request.POST["password"],
        )
        if user is None:
            template_dict["is_error"] = True
            user = CustomUser.objects.get_or_none(user_id=request.POST["user_id"])
            if user is not None:
                if user.is_active is False:
                    template_dict["is_user_inactive"] = True
            return render(request, login_page, template_dict)
        else:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/home")
            else:
                template_dict["is_user_inactive"] = True
                return render(request, login_page, template_dict)

    return render(request, login_page, template_dict)


def get_app_config_obj():
    app_config_obj = {}
    app_config = checkpoint.objects.get_or_none(cp_type="app_config")
    if app_config is not None:
        cp_details = app_config.cp_details
        for key, value in cp_details.items():
            app_config_obj[key] = value[0]
    return app_config_obj

import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from cwf.models import checkpoint, CustomUser
from cwf.utils import get_environment, is_ajax_request
from django.contrib.auth.decorators import login_required


def show_homepage(request):
    print("request host: ", request.get_host())
    if request.method == "POST":
        print("got post showing login page")
        return show_login_page(request)
    if request.get_host().find("cnx") != -1 or request.get_host().find("cinex2") != -1:
        print("shwoing cnx home page")
        return render(request, "cwf/cnx/cnx_home_page.html")

    print("no post, no home, last return showing login")
    return show_login_page(request)


def show_login_page(request):

    if request.user.is_authenticated:
        print("redirecting to home...!")
        return HttpResponseRedirect("/home")

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
    print("template_dict: ", template_dict)

    if request.method == "POST":
        user = authenticate(
            user_id=request.POST["user_id"], password=request.POST["password"]
        )
        print("user: ", user)
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
                print("redirecting to home...!")
                return HttpResponseRedirect("/home.html")
            else:
                template_dict["is_user_inactive"] = True
                return render(request, login_page, template_dict)

    return render(request, login_page, template_dict)


def onboard_user(request):
    if not is_ajax_request(request):
        return

    if request.method == "POST":
        signup_obj = json.loads(request.body)
        usr_name = signup_obj["usr_name"]
        usr_name_list = usr_name.split(" ")
        first_name = usr_name_list[0]
        last_name = usr_name_list[-1]
        usr_email = signup_obj["usr_email"]
        usr_pswd = signup_obj["usr_pswd"]

        user_rec = CustomUser.objects.get_or_none(user_id=usr_email)

        if user_rec:
            print("User exist!")
            return show_login_page(request)

        user_rec = CustomUser()
        user_rec.user_id = usr_email
        user_rec.first_name = first_name
        user_rec.last_name = last_name
        user_rec.email = usr_email
        user_rec.login_type = "local"
        user_rec.is_active = True
        user_rec.is_superuser = True
        user_rec.is_staff = True
        user_rec.set_password(usr_pswd)
        user_rec.other_details = {}
        user_rec.save()

        return render(request, template_name="cwf/cnx/cnx_login.html")

    return render(request, template_name="cwf/login.html")


def get_app_config_obj():
    app_config_obj = {}
    app_config = checkpoint.objects.get_or_none(cp_type="app_config")
    if app_config is not None:
        cp_details = app_config.cp_details
        for key, value in cp_details.items():
            app_config_obj[key] = value[0]
    return app_config_obj


@login_required
def index(request):
    # client = Client.objects.get_or_none(schema_name=connection.schema_name)
    environment = get_environment(request)
    template_dict = {
        "env": environment,
        "current_user": request.user,
        # "schema_name": client.schema_name,
        "app_config": get_app_config_obj(),
    }
    required_params = get_required_params()
    other_details = {}
    for key, value in required_params.items():
        template_dict[key] = other_details.get(key, value)

    return render(request, "cwf/home.html", template_dict)


def get_required_params():
    return {
        "app_init_process": "",
        "offline_data_enabled": "no",
        "input_field_border": "",
        "solution_short_name": "",
        "color_theme": "theme-default",
    }

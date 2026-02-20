import json
from django.shortcuts import render


def insertion_page(request):
    """renders cinex insertion"""
    template_name = "cnx/cnx_insertion.html"

    template_dict = {}

    return render(request, template_name, template_dict)

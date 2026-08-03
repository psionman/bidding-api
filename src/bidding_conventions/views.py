import json

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.generic import TemplateView

import bidding_conventions.application as app


def handle_request(request, func, *args) -> JsonResponse:
    req = json.loads(request.body or b"{}")
    return JsonResponse(func(req, *args), safe=False)


@ensure_csrf_cookie
@never_cache
def ensure_csrf(request):
    token = get_token(request)
    return JsonResponse({"status": "ok", "csrftoken": token})


@method_decorator(csrf_exempt, name="dispatch")
class StaticData(View):
    def get(self, request):
        print("StaticData.getd")
        return JsonResponse(
            app.static_data(request.META.get("REMOTE_ADDR")), safe=False
        )


@method_decorator(csrf_exempt, name="dispatch")
class GetConventions(View):
    def post(self, request):
        return handle_request(request, app.get_conventions)


@method_decorator(csrf_exempt, name="dispatch")
class ConventionsSelected(View):
    def post(self, request):
        return handle_request(request, app.conventions_selected)


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"

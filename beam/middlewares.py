from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from applications.global_settings.models import DisabledAPI
from beam import messages


class APIMaintenanceMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response
        self.admin_url = "/boomerang-post-admin-panel/secret/"

    def __call__(self, request):
        self.disabled_api = DisabledAPI.objects.first()
        response = self.process_request(request)
        if response is None and callable(self.get_response):
            response = self.get_response(request)
        return response

    def _need_maintenance_response(self, request) -> bool:
        if (
            self.disabled_api
            and self.disabled_api.disable
            and not request.path.startswith(self.admin_url)
        ):
            return True
        else:
            return False

    def process_request(self, request):
        if self._need_maintenance_response(request):
            return HttpResponse(messages.MAINTENANCE_WORK_IN_PROGRESS, status=503)
        return None
    
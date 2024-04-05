from ninja_extra import NinjaExtraAPI
from WebCamAPI.api_contoller import CameraController
from ninja_extra import NinjaExtraAPI
from ninja.security import APIKeyHeader
from ninja.security import django_auth


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        if key == "supersecret":
            return key


header_key = ApiKey()

#api = NinjaExtraAPI(title="WebCamAPI", version="0.0.1", csrf=True, auth=[header_key, django_auth])
api = NinjaExtraAPI(title="WebCamAPI", version="0.0.1")
api.register_controllers(CameraController)

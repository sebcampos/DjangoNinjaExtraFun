from ninja_extra import NinjaExtraAPI
from WebCamAPI.api_contoller import CameraController

api = NinjaExtraAPI(title="WebCamAPI", version="0.0.1")
api.register_controllers(CameraController)
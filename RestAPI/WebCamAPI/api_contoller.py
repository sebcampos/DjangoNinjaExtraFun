from ninja_extra import (
    http_get, http_post, http_generic, http_delete,
    api_controller, status, ControllerBase, pagination, route
)
from ninja_extra.controllers.response import Detail
from asgiref.sync import sync_to_async
from . import models, schemas, OBJECT_DETECTION_MODEL_LABELS


def get_tracked_and_untracked_objects() -> dict:
    tracking_model_instance = models.TrackingObjects.objects.first()
    if tracking_model_instance is None:
        tracking_model_instance = models.TrackingObjects.objects.create()
    tracked = [i.attname for i in tracking_model_instance._meta.get_fields() if
               i.attname != "id" and tracking_model_instance.__getattribute__(i.attname) == True]
    untracked = [i for i in OBJECT_DETECTION_MODEL_LABELS.values() if i not in tracked]
    return {
        "tracked": tracked,
        "untracked": untracked
    }


@api_controller('/cam')
class CameraController(ControllerBase):
    event_model = models.ObjectDetectionEvent
    tracking_model = models.TrackingObjects

    @route.get("/events", response=pagination.PaginatedResponseSchema[schemas.ObjectDetectionEventResponseSchema])
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=50)
    async def list_events(self):
        return self.event_model.objects.all()

    @route.post("/events/", response=schemas.ObjectDetectionEventResponseSchema)
    async def create_events(self, event: schemas.ObjectDetectionEventCreateSchema):
        return await sync_to_async(self.event_model.objects.create)(object_index=event.object_index)

    @route.put("/events/{str:event_uuid}/", response=schemas.ObjectDetectionEventResponseSchema)
    async def update_event(self, event_uuid: str, new_event_data: schemas.ObjectDetectionEventUpdateSchema):
        event = await self.event_model.objects.aget(event_id=event_uuid)
        event.event_occurring = new_event_data.event_occurring
        await event.asave()
        return event

    @route.get("/events/{str:event_uuid}", response=schemas.ObjectDetectionEventResponseSchema)
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=50)
    async def get_event(self, event_uuid: str):
        return self.event_model.objects.filter(event_uuid=event_uuid)

    @route.get("/track", response=schemas.TrackingObjectsResponseSchema)
    async def display_tracking_settings(self):
        return await sync_to_async(get_tracked_and_untracked_objects)()

    @route.put("/track", response=schemas.TrackingObjectsResponseSchema)
    async def list_tracking(self, tracking_payload: schemas.TrackingObjectsUpdateRequestSchema):
        tracking_settings = await sync_to_async(self.tracking_model.objects.first)()
        if tracking_payload.track is not None:
            for event in tracking_payload.track:
                tracking_settings.__setattr__(event, True)
        if tracking_payload.untrack is not None:
            for event in tracking_payload.track:
                tracking_settings.__setattr__(event, False)
        await tracking_settings.asave()
        return await sync_to_async(get_tracked_and_untracked_objects)()

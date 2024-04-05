from ninja import ModelSchema, Schema
from enum import Enum
from typing import List
from . import models


class EventLabelsEnum(str, Enum):
    unknown_0 = 'unknown_0'
    person = 'person'
    bicycle = 'bicycle'
    car = 'car'
    motorcycle = 'motorcycle'
    airplane = 'airplane'
    bus = 'bus'
    train = 'train'
    truck = 'truck'
    boat = 'boat'
    traffic = 'traffic'
    light = 'light'
    fire = 'fire'
    hydrant = 'hydrant'
    unknown_1 = 'unknown_1'
    stop = 'stop'
    sign = 'sign'
    parking = 'parking'
    meter = 'meter'
    bench = 'bench'
    bird = 'bird'
    cat = 'cat'
    dog_0 = 'dog_0'
    horse = 'horse'
    sheep = 'sheep'
    cow = 'cow'
    elephant = 'elephant'
    bear_0 = 'bear_0'
    zebra = 'zebra'
    giraffe = 'giraffe'
    unknown_2 = 'unknown_2'
    backpack = 'backpack'
    umbrella = 'umbrella'
    unknown_3 = 'unknown_3'
    unknown_4 = 'unknown_4'
    handbag = 'handbag'
    tie = 'tie'
    suitcase = 'suitcase'
    frisbee = 'frisbee'
    skis = 'skis'
    snowboard = 'snowboard'
    sports = 'sports'
    ball = 'ball'
    kite = 'kite'
    baseball_0 = 'baseball_0'
    bat = 'bat'
    baseball_1 = 'baseball_1'
    glove = 'glove'
    skateboard = 'skateboard'
    surfboard = 'surfboard'
    tennis = 'tennis'
    racket = 'racket'
    bottle = 'bottle'
    unknown_5 = 'unknown_5'
    wine = 'wine'
    glass = 'glass'
    cup = 'cup'
    fork = 'fork'
    knife = 'knife'
    spoon = 'spoon'
    bowl = 'bowl'
    banana = 'banana'
    apple = 'apple'
    sandwich = 'sandwich'
    orange = 'orange'
    broccoli = 'broccoli'
    carrot = 'carrot'
    hot = 'hot'
    dog_1 = 'dog_1'
    pizza = 'pizza'
    donut = 'donut'
    cake = 'cake'
    chair = 'chair'
    couch = 'couch'
    potted = 'potted'
    plant = 'plant'
    bed = 'bed'
    unknown_6 = 'unknown_6'
    dining = 'dining'
    table = 'table'
    unknown_7 = 'unknown_7'
    unknown_8 = 'unknown_8'
    toilet = 'toilet'
    unknown_9 = 'unknown_9'
    tv = 'tv'
    laptop = 'laptop'
    mouse = 'mouse'
    remote = 'remote'
    keyboard = 'keyboard'
    cell = 'cell'
    phone = 'phone'
    microwave = 'microwave'
    oven = 'oven'
    toaster = 'toaster'
    sink = 'sink'
    refrigerator = 'refrigerator'
    unknown_10 = 'unknown_10'
    book = 'book'
    clock = 'clock'
    vase = 'vase'
    scissors = 'scissors'
    teddy = 'teddy'
    bear_1 = 'bear_1'
    hair = 'hair'
    drier = 'drier'
    toothbrush = 'toothbrush'
    empty = 'empty'


class ObjectDetectionEventCreateSchema(ModelSchema):
    class Config:
        model = models.ObjectDetectionEvent
        model_fields = ["object_index"]


class ObjectDetectionEventUpdateSchema(ModelSchema):
    class Meta:
        model = models.ObjectDetectionEvent
        exclude = ["object_index", "event_id"]


class ObjectDetectionEventResponseSchema(ModelSchema):
    object_name: str
    duration: float

    class Config:
        model = models.ObjectDetectionEvent
        model_fields = "__all__"


class TrackingObjectsResponseSchema(Schema):
    tracked: List[EventLabelsEnum]
    untracked: List[EventLabelsEnum]


class TrackingObjectsUpdateRequestSchema(Schema):
    track: List[EventLabelsEnum] | None = None
    untrack: List[EventLabelsEnum] | None = None

import uuid
from datetime import datetime, timezone
from django.db import models
from . import OBJECT_DETECTION_MODEL_LABELS


class EventLabelIndexChoices(models.IntegerChoices):
    unknown_0 = 0
    person = 1
    bicycle = 2
    car = 3
    motorcycle = 4
    airplane = 5
    bus = 6
    train = 7
    truck = 8
    boat = 9
    traffic = 10
    light = 11
    fire = 12
    hydrant = 13
    unknown_1 = 14
    stop = 15
    sign = 16
    parking = 17
    meter = 18
    bench = 19
    bird = 20
    cat = 21
    dog_0 = 22
    horse = 23
    sheep = 24
    cow = 25
    elephant = 26
    bear_0 = 27
    zebra = 28
    giraffe = 29
    unknown_2 = 30
    backpack = 31
    umbrella = 32
    unknown_3 = 33
    unknown_4 = 34
    handbag = 35
    tie = 36
    suitcase = 37
    frisbee = 38
    skis = 39
    snowboard = 40
    sports = 41
    ball = 42
    kite = 43
    baseball_0 = 44
    bat = 45
    baseball_1 = 46
    glove = 47
    skateboard = 48
    surfboard = 49
    tennis = 50
    racket = 51
    bottle = 52
    unknown_5 = 53
    wine = 54
    glass = 55
    cup = 56
    fork = 57
    knife = 58
    spoon = 59
    bowl = 60
    banana = 61
    apple = 62
    sandwich = 63
    orange = 64
    broccoli = 65
    carrot = 66
    hot = 67
    dog_1 = 68
    pizza = 69
    donut = 70
    cake = 71
    chair = 72
    couch = 73
    potted = 74
    plant = 75
    bed = 76
    unknown_6 = 77
    dining = 78
    table = 79
    unknown_7 = 80
    unknown_8 = 81
    toilet = 82
    unknown_9 = 83
    tv = 84
    laptop = 85
    mouse = 86
    remote = 87
    keyboard = 88
    cell = 89
    phone = 90
    microwave = 91
    oven = 92
    toaster = 93
    sink = 94
    refrigerator = 95
    unknown_10 = 96
    book = 97
    clock = 98
    vase = 99
    scissors = 100
    teddy = 101
    bear_1 = 102
    hair = 103
    drier = 104
    toothbrush = 105
    empty = 106


# Create your models here.
class ObjectDetectionEvent(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    event_occurring = models.BooleanField(default=True)
    object_index = models.IntegerField(choices=EventLabelIndexChoices.choices)

    @property
    def object_name(self) -> str:
        return OBJECT_DETECTION_MODEL_LABELS[self.object_index]

    @property
    def duration(self) -> float:
        print(datetime.now(timezone.utc), self.start_time)
        if self.end_time is None:
            return (datetime.now(timezone.utc) - self.start_time).total_seconds()
        return (self.end_time - self.start_time).total_seconds()


class TrackingObjects(models.Model):
    unknown_0 = models.BooleanField(default=False)
    person = models.BooleanField(default=False)
    bicycle = models.BooleanField(default=False)
    car = models.BooleanField(default=False)
    motorcycle = models.BooleanField(default=False)
    airplane = models.BooleanField(default=False)
    bus = models.BooleanField(default=False)
    train = models.BooleanField(default=False)
    truck = models.BooleanField(default=False)
    boat = models.BooleanField(default=False)
    traffic = models.BooleanField(default=False)
    light = models.BooleanField(default=False)
    fire = models.BooleanField(default=False)
    hydrant = models.BooleanField(default=False)
    unknown_1 = models.BooleanField(default=False)
    stop = models.BooleanField(default=False)
    sign = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    meter = models.BooleanField(default=False)
    bench = models.BooleanField(default=False)
    bird = models.BooleanField(default=False)
    cat = models.BooleanField(default=False)
    dog_0 = models.BooleanField(default=False)
    horse = models.BooleanField(default=False)
    sheep = models.BooleanField(default=False)
    cow = models.BooleanField(default=False)
    elephant = models.BooleanField(default=False)
    bear_0 = models.BooleanField(default=False)
    zebra = models.BooleanField(default=False)
    giraffe = models.BooleanField(default=False)
    unknown_2 = models.BooleanField(default=False)
    backpack = models.BooleanField(default=False)
    umbrella = models.BooleanField(default=False)
    unknown_3 = models.BooleanField(default=False)
    unknown_4 = models.BooleanField(default=False)
    handbag = models.BooleanField(default=False)
    tie = models.BooleanField(default=False)
    suitcase = models.BooleanField(default=False)
    frisbee = models.BooleanField(default=False)
    skis = models.BooleanField(default=False)
    snowboard = models.BooleanField(default=False)
    sports = models.BooleanField(default=False)
    ball = models.BooleanField(default=False)
    kite = models.BooleanField(default=False)
    baseball_0 = models.BooleanField(default=False)
    bat = models.BooleanField(default=False)
    baseball_1 = models.BooleanField(default=False)
    glove = models.BooleanField(default=False)
    skateboard = models.BooleanField(default=False)
    surfboard = models.BooleanField(default=False)
    tennis = models.BooleanField(default=False)
    racket = models.BooleanField(default=False)
    bottle = models.BooleanField(default=False)
    unknown_5 = models.BooleanField(default=False)
    wine = models.BooleanField(default=False)
    glass = models.BooleanField(default=False)
    cup = models.BooleanField(default=False)
    fork = models.BooleanField(default=False)
    knife = models.BooleanField(default=False)
    spoon = models.BooleanField(default=False)
    bowl = models.BooleanField(default=False)
    banana = models.BooleanField(default=False)
    apple = models.BooleanField(default=False)
    sandwich = models.BooleanField(default=False)
    orange = models.BooleanField(default=False)
    broccoli = models.BooleanField(default=False)
    carrot = models.BooleanField(default=False)
    hot = models.BooleanField(default=False)
    dog_1 = models.BooleanField(default=False)
    pizza = models.BooleanField(default=False)
    donut = models.BooleanField(default=False)
    cake = models.BooleanField(default=False)
    chair = models.BooleanField(default=False)
    couch = models.BooleanField(default=False)
    potted = models.BooleanField(default=False)
    plant = models.BooleanField(default=False)
    bed = models.BooleanField(default=False)
    unknown_6 = models.BooleanField(default=False)
    dining = models.BooleanField(default=False)
    table = models.BooleanField(default=False)
    unknown_7 = models.BooleanField(default=False)
    unknown_8 = models.BooleanField(default=False)
    toilet = models.BooleanField(default=False)
    unknown_9 = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)
    laptop = models.BooleanField(default=False)
    mouse = models.BooleanField(default=False)
    remote = models.BooleanField(default=False)
    keyboard = models.BooleanField(default=False)
    cell = models.BooleanField(default=False)
    phone = models.BooleanField(default=False)
    microwave = models.BooleanField(default=False)
    oven = models.BooleanField(default=False)
    toaster = models.BooleanField(default=False)
    sink = models.BooleanField(default=False)
    refrigerator = models.BooleanField(default=False)
    unknown_10 = models.BooleanField(default=False)
    book = models.BooleanField(default=False)
    clock = models.BooleanField(default=False)
    vase = models.BooleanField(default=False)
    scissors = models.BooleanField(default=False)
    teddy = models.BooleanField(default=False)
    bear_1 = models.BooleanField(default=False)
    hair = models.BooleanField(default=False)
    drier = models.BooleanField(default=False)
    toothbrush = models.BooleanField(default=False)
    empty = models.BooleanField(default=False)

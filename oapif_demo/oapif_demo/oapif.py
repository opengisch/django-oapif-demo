from django_oapif import OAPIF
from django_oapif.auth import BasicAuth, DjangoAuth

from .models import Apiary, Area, PollenConsumption, Review, Track

oapif = OAPIF(auth=[BasicAuth(), DjangoAuth()])

oapif.register_collection(Apiary)
oapif.register_collection(Area)
oapif.register_collection(Track)
oapif.register_collection(Review)
oapif.register_collection(PollenConsumption)

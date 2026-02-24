

from django_oapif import OAPIF
from django_oapif.auth import BasicAuth, DjangoAuth

from .models import Apiary, Area, PollenConsumption, Reviews, Tracks

oapif = OAPIF(auth=[BasicAuth(), DjangoAuth()])

oapif.register_collection(Apiary)
oapif.register_collection(Area)
oapif.register_collection(Tracks)
oapif.register_collection(Reviews)
oapif.register_collection(PollenConsumption)

from django.test import TestCase
import requests
import time
import json

"""
All'interno di questo file vengono riportate i test case necessari per stabilire il corretto funzionamento dell'API
REST fornita dal Job Processor. A tal fine e' necessario che il server Celery e Flower siano stati avviati correttamente.
I test vengono effettuati sui task di un'applicazione di esempio precedentemente definita (sample_app).
"""

# si suppone che il server Django sia stato avviato al seguente endpoint
DJANGO_ENDPOINT = "http://localhost:8000/"

# test per deteminare se le API REST definite sono state implementate correttamente
# e' necessario avviare sia celery che flower per testare il funzionamento corretto
# TODO definire un'applicazione di esempio sulla quale lanciare dei task di prova
# nell'applicazione di prova si riporta anche la struttura di esempio che deve avere un'applicazione



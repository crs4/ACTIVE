from django.db import models

""" classi wrapper di quelle originarie utilizzate da notreDAM """

class Person(models.Model):
    GENDER_CHOICE = ((u'M', u'Male'), (u'F', u'Female'))

    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    birth_date  = models.DateField()
    gender      = models.CharField(max_length=3, choices=GENDER_CHOICE)
    description = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name

class Item(models.Model):
    name     = models.CharField(max_length=200)
    path     = models.CharField(max_length=200)
    metadata = models.CharField(max_length=200, blank=True)
    """ mancano i metodi per la manipolazione degli attributi degli item """

    def __unicode__(self):
        return self.name + " - " + self.path

    def __str__(self):
        return self.name + " - " + self.path

"""
Classe che consente di organizzare i metadati relativi alle occorrenze di una
particolare persona all'interno di un contenuto digitale.
Gli attributi riportanti l'istante di inizio e la durata non sono presenti nel
caso delle immagini mentre devono essere sempre presenti nel caso di audio e video.
Se invece si considera un file audio non si deve indicare i valori degli attributi
x ed y, necessari nel caso di video e immagini.
"""
class Occurrence(models.Model):
    person      = models.ForeignKey(Person)
    item        = models.ForeignKey(Item)
    position_x  = models.PositiveIntegerField()
    position_y  = models.PositiveIntegerField()
    """ millisecondi trascorsi dall'inizio del video/audio???? """
    start_time  = models.TimeField("Occurrence start")
    """ millisecondi??? """
    length      = models.TimeField("Occurence duration")

""" gestire il polimorfismo a oggetti??? con Django! """
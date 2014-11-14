from django.db import models

# le classi riportate in questo file corrispondono a dei
# wrapper di quelle originarie utilizzate all'interno di notreDAM
# vengono riportate per consentire l'interoperabilita' tra le diverse funzionalita'
# sviluppate, indicando solamente gli attributi essenziali

"""
Classe riportante le informazioni associate a una persona, in questo modo
e' possibile fare riferimento ad informazioni aggiuntive sulle persone che
vengono identificate all'interno dei video.
TODO decidere se estendere il modello alle entita' (persone, cose, animali)
TODO consentire inizialmente dei valori nulli nei campi
"""
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


"""
Classe riportante le informazioni di un particolare item (un generico contenuto
digitale che viene memorizzato, catalogato e indicizzato dal DAM.
Vengono riportate le principali informazioni associate a un item.
"""
class Item(models.Model):
    name     = models.CharField(max_length=200)
    path     = models.CharField(max_length=200)
    # per semplicita' i metadati vengono riporatati come una stringa
    metadata = models.CharField(max_length=200, blank=True)
    # mancano i metodi per la manipolazione degli attributi degli item

    def __unicode__(self):
        return self.name + " - " + self.path

    def __str__(self):
        return self.name + " - " + self.path

"""
Classe che consente di organizzare i metadati relativi alle occorrenze di una
persona all'interno di un contenuto digitale (item).
Alcuni degli attributi riportati possono assumere valore nullo, sulla base della
tipologia di contenuto digitale che viene considerato.
Ad esempio per immagini e video ha senso riportare le informazioni sulla posizione
mentre per i contenuti audio no...
"""
class Occurrence(models.Model):
    person      = models.ForeignKey(Person)
    item        = models.ForeignKey(Item)
    # posizione all'interno di un'immagine in cui viene determinato un volto
    position_x  = models.PositiveIntegerField(blank=True)
    position_y  = models.PositiveIntegerField(blank=True)
    position_width  = models.PositiveIntegerField(blank=True)
    position_height = models.PositiveIntegerField(blank=True)
    # millisecondi trascorsi dall'inizio del video/audio????
    start_time  = models.TimeField(null=True)
    # durata di un'apparizione espressa in millisecondi???
    length      = models.TimeField(null=True)


####################################################################################
# TODO gestire il polimorfismo delle classi in python/Django                       #
# in particolare sarebbe utile definire delle classi che riportano                 #
# le informazioni delle occorrenze sulla base della tipologia di item considerato. #
####################################################################################
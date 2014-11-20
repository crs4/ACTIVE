from django.db import models

# le classi riportate in questo file corrispondono a dei
# wrapper di quelle originarie utilizzate all'interno di notreDAM
# vengono riportate per consentire l'interoperabilita' tra le diverse funzionalita'
# sviluppate, indicando solamente gli attributi essenziali

"""
This class contains all information  associated to a person, so it will be possible to
retrieve his extra information.
It is possible to create anonymous persons, that will be identified lately by a user; so
some fields could have a null value.

TODO decidere se estendere il modello alle entita' (persone, cose, animali)
"""
class Person(models.Model):
    GENDER_CHOICE = ((u'M', u'Male'), (u'F', u'Female'))

    first_name  = models.CharField(max_length=100, blank=True)
    last_name   = models.CharField(max_length=100, blank=True)
    birth_date  = models.DateField(null=True)
    gender      = models.CharField(max_length=2, choices=GENDER_CHOICE, blank=True)
    description = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return " ".join((self.first_name, self.last_name))

    def __str__(self):
        return " ".join((self.first_name, self.last_name))

    # funzione utilizzata per ovviare al problema della serializzazione (non consente un controllo
    # totale sugli attributi generati) da correggere/rimuovere!
    def __json__(self):
        list = {}
        list['id']          = self.pk
        list['first_name']  = self.first_name
        list['last_name']   = self.last_name
        list['gender']      = self.gender
        list['birth_date']  = str(self.birth_date)
        list['description'] = self.description
        return list

"""
This class contains all information about an item (a generic digital content) stored,
catalogued and indexed by the DAM.
Here only main attributes has been specified; a more complete data model is provided by the DAM
"""
class Item(models.Model):
    name     = models.CharField(max_length=200)
    path     = models.CharField(max_length=200)
    # per semplicita' i metadati vengono riporatati come una stringa
    metadata = models.CharField(max_length=200, blank=True)
    # mancano i metodi per la manipolazione degli attributi degli item

    def __unicode__(self):
        return " ".join((self.path, self.name))

    def __str__(self):
        return " ".join((self.path, self.name))

    # funzione utilizzata per ovviare al problema della serializzazione (non consente un controllo
    # totale sugli attributi generati) da correggere/rimuovere!
    def __json__(self):
        list = {}
        list['id']          = self.pk
        list['name']        = self.name
        list['path']        = self.path
        list['metadata']    = self.metadata
        return list

"""
This class is used to organize metadata referred to persons detected inside a digital content (item)
Some attributes could bu null, depending on digital content type.
For example images and videos it is useful to specify position data; for audio files any kind of positional
data is useless and nonsense.
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
    start_time  = models.BigIntegerField(blank=True, null=True)
    # durata di un'apparizione espressa in millisecondi???
    length      = models.BigIntegerField(blank=True, null=True)

    def __unicode__(self):
        return " - ".join((self.person.__str__(), self.item.__str__()))

    def __str__(self):
        return " - ".join((self.person.__str__(), self.item.__str__()))

    # funzione utilizzata per ovviare al problema della serializzazione (non consente un controllo
    # totale sugli attributi generati) da correggere/rimuovere!
    def __json__(self):
        list = {}
        list['id']          = self.pk
        list['person_id']   = self.person.pk
        list['item_id']     = self.item.pk
        list['position_x']  = self.position_x
        list['position_y']  = self.position_y
        list['position_width'] = self.position_width
        list['position_height']= self.position_height
        list['start_time']  = self.start_time
        list['length']      = self.length
        return list
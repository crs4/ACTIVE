.. ACTIVE documentation master file, created by
   sphinx-quickstart on Tue Jun 10 10:06:57 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



 {% extends "!layout.html" %}


    {% block rootrellink %}
            <li><a href="{{ pathto('index') }}">home</a>|&nbsp;</li>
            <li><a href="{{ pathto('search') }}">search</a>|&nbsp;</li>
           <li><a href="{{ pathto('contents') }}">documentation </a> &raquo;</li>
    {% endblock %}


    {% block relbar1 %}

    <div style="background-color: white; text-align: left; padding: 10px 10px 15px 15px">
    <a href="{{ pathto('index') }}"><img src="{{ pathto('_static/mare.png', 1) }}" border="0" alt="ACTIVE"/></a>
    </div>
    {{ super() }}
    {% endblock %}



Welcome to ACTIVE's documentation!
==================================

Contents:

Il progetto [ACTIVE]_ (Automatic Classification Tools for the Intelligent Video Ecosystem) intende realizzare una piattaforma di catalogazione intelligente mirata a valorizzare gli archivi audiovisuali di imprese che operano nell'ambito dell'industria dei contenuti, sia a livello di produzione che di distribuzione.



.. toctree::

   tools
   prova.html



The :mod:`toolsAPI` Module
-------------------------

THIS IS THE PROGRAMMATIC API

.. automodule:: toolsAPI
   :members:
   :show-inheritance:	

The :mod:`face_extractor` Module
-------------------------
.. automodule:: face_extractor
   :members:
   :show-inheritance:

The :mod:`Constants` Module
-------------------------
.. automodule:: Constants
   :members:
   :show-inheritance:

The :mod:`face_detection` Module
-------------------------
.. automodule:: face_detection
   :members:
   :show-inheritance:

The :mod:`Utils` Module
-------------------------
.. automodule:: Utils
   :members:
   :show-inheritance:

The :mod:`face_recognition` Module
-------------------------
.. automodule:: face_recognition
   :members:

The :mod:`crop_face` Module
-------------------------
.. automodule:: crop_face
   :members:

The :mod:`FaceModelsLBP` Module
-------------------------
.. automodule:: FaceModelsLBP
   :members:

The :mod:`Utils` Module
-------------------------
.. automodule:: Utils
   :members:


Tutorials
^^^^^^^^^^^^^^^^^^^^^^^^^^^


   `yahoo <http://yahoo.com>`_
	






.. [ACTIVE] www.active……


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


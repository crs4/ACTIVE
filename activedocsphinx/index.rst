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
   test.test_module



The :mod:`caption_recognition` Module
-------------------------------------
.. automodule:: caption_recognition
   :members:
   :show-inheritance:
   
The :mod:`face_detection` Module
--------------------------------
.. automodule:: face_detection
   :members:
   :show-inheritance:
   
The :mod:`face_models` Module
-----------------------------
.. automodule:: face_models
   :members:
   :show-inheritance:
   
The :mod:`utils` Module
-----------------------
.. automodule:: utils
   :members:
   :show-inheritance:
   
The :mod:`video_face_extractor` Module
--------------------------------------
.. automodule:: video_face_extractor
   :members:
   :show-inheritance:
   
The :mod:`caption_software_test` Module
--------------------------------------
.. automodule:: caption_software_test
   :members:
   :show-inheritance:
   
The :mod:`caption_test` Module
--------------------------------------
.. automodule:: caption_test
   :members:
   :show-inheritance:


.. [ACTIVE] http://active.crs4.it/


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


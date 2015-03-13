# Listener di signals
# intercettare i signal ed il sender che vengono sollevati
# cerca gli eventi associati al signal
# trova i plugin associati a ciascun eventi
# invoca i plugin sul jobprocessor, passando i parametri
#
#
# TODO aggiungere i parametri alle chiamate delle funzioni
#

from core.plugins.models import Event, View, Plugin

class EventManager():

	def start_plugins(self, event_name):
		# ottiene i plugin associati a un evento e li invoca (jp)
		if (Plugin.objects.filter(events__name = event_name).count() > 0):
			for plugin in Plugin.objects.filter(events__name = event_name):
				print plugin.title
				self.execute_plugin()
		# determina che non si tratta di un plugin
		else:
			pass

	def start_plugins_by_view(self, view_name):
		# ottiene gli eventi associati a una vista
		for view in View.objects.filter(path_abs = view_name):
			print view.path_abs
			self.start_plugins(view.event.name)
	
	def execute_plugin(self):
		# invoca il job processor per eseguire il plugin
		pass


define(["core/module"], function (module) {

    "use strict";

    module.registerFactory("Mediator", function ($rootScope) {
		
		return {
			
			mediateContextMenuEvent: function(widgetContextModel){
				$rootScope.$broadcast("contextMenu", {widgetContextModel:widgetContextModel});
			},

			mediateSelectedItems: function(selectedItems){
				$rootScope.$broadcast("selectedItems", {selectedItems:selectedItems});
			},

			mediateUnselectItems: function(){
				$rootScope.$broadcast("unselectItems");
			},

			mediateSelectedModel: function(selectedModel){
				$rootScope.$broadcast("selectedModel", {selectedModel:selectedModel});
			},

			mediateBindInstance: function(){
				$rootScope.$broadcast("bindInstance");
			},
			
		}
		
	});
	
});

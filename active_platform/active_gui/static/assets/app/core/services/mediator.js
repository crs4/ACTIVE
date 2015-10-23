define(["core/module"], function (module) {

    "use strict";

    module.registerFactory("Mediator", function ($rootScope) {
		
		return {
			
			mediateSelectedItems: function(selectedItems){
				$rootScope.$broadcast("selectedItems", {selectedItems:selectedItems});
			},
			
			mediateUnselectItems: function(){
				$rootScope.$broadcast("unselectItems");
			},
			
			mediateSelectedType: function(selectedType){
				$rootScope.$broadcast("typeUpdated", {selectedType:selectedType});
			},
			
			mediateSelectedScript: function(selectedScript){
				$rootScope.$broadcast("selectedScript", {selectedScript:selectedScript});
			},
			
			mediateLoadedScripts: function(loadedScripts){
				$rootScope.$broadcast("loadedScripts", {loadedScripts:loadedScripts});
			},
			
			mediateExecuteScript: function(){
				$rootScope.$broadcast("executeScript");
			},
			
			mediateAfterExecuteScript: function(){
				$rootScope.$broadcast("afterExecuteScript", {});
			},
			
			mediateContextMenuEvent: function(widgetContextModel){
				$rootScope.$broadcast("contextMenu", {widgetContextModel:widgetContextModel});
			},
			
			mediateElementReady: function(elm){
				$rootScope.$broadcast("elementReady", {element:elm});
			},
			
			mediateSidebarChange: function(selected){
				$rootScope.$broadcast("sidebarChanged", {selected:selected});
			},

			mediateEnableSummarizer: function(personId){
				$rootScope.$broadcast("enable_summarizer", {personId:personId});
			},

			mediateEnableNavigator: function(itemId){
				$rootScope.$broadcast("enable_navigator", {itemId:itemId});
			}
			
		}
		
	});
	
});

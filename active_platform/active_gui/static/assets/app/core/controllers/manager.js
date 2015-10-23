define(["core/module"], function (module) {

    "use strict";

    module.registerController("managerCtrl", function ($scope, $stateParams, Mediator, coreService) {
		
		$scope.selectedItems = [];
		$scope.plugins = [];
		$scope.selectedScript = null;
		$scope.selectedType = $stateParams.type;
		
		$scope.$on("selectedItems", function(event, args){
			$scope.selectedItems = args.selectedItems;
		});
		
		$scope.$on("afterExecuteScript", function(event, args){
			$scope.selectedScript = null;
			angular.element("#s2").select2("val", null);
		});
		
		$scope.$watch("selectedScript", function(newValue, oldValue){
			Mediator.mediateSelectedScript($scope.selectedScript);
		});
		
		$scope.executeScript = function(){
			Mediator.mediateExecuteScript();
		};
		
		$scope.unselectItems = function() {
			$scope.selectedItems.length = 0;
			Mediator.mediateUnselectItems();
		};
		
		var s = coreService.Script.query(function(){
			$scope.plugins = parseScripts(s);
			Mediator.mediateLoadedScripts($scope.plugins);
		});
		
		var containsObject = function(obj, list) {
			var i;
			for (i = 0; i < list.length; i++) {
				if (angular.equals(list[i].id, obj.id)) {
					return true;
				}
			}
			return false;
		};
		
		var parseScripts = function(scripts){
			var plugins = [];
			for(var i = 0; i < scripts.length; i++){
				var p = scripts[i].plugin;
				if(!containsObject(p, plugins)){
					p["scripts"] = [];
					plugins.push(p);
				}
			}
			for(var i = 1; i < plugins.length;){
				if(plugins[i-1].id === plugins[i].id){
					plugins.splice(i, 1);
				} else {
					i++;
				}
			}
			for(var i = 0; i < plugins.length; i++){
				for(var j = 0; j < scripts.length; j++){
					if(plugins[i].name === scripts[j].plugin.name){
						plugins[i].scripts.push(scripts[j]);
					}
				}
			}
			//TODO: eliminare plugin da ogni script
			return plugins;
		};	
		
	});
    
});

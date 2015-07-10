define(["core/module"], function(module){
	
	"use strict";
		
	module.registerController("permissionCtrl", function($scope, coreService){
		
		$scope.getElement(coreService.Permission);
		
		$scope.$on("sidebarChanged", function(event, args){
			setCodeName();
			setContentType(args.selected);
		});
		
		var setCodeName = function(){
			$scope.currentElement.codename = $scope.currentElement.name.replace (/\s+/g, "_");
			$scope.currentElement.codename.toLowerCase();
		};
		
		var setContentType = function(content_types){
			$scope.currentElement.content_type = content_types[0];
		};
		
	});
	
});

define(["core/module"], function(module){
	
	"use strict";
		
	module.registerController("groupTableCtrl", function($scope, coreService){
		
		$scope.$watch("gridOptions.currentPage", function(){
			$scope.$emit("fetchPage", {service:coreService.Group});
		});
		
		$scope.removeRow = function(row){
			$scope.$emit("removeRow", {service:coreService.Group, row:row});
		};
		
	});
	
});

define(["core/module"], function(module){
	
	"use strict";
		
	module.registerController("permissionTableCtrl", function($scope, coreService){
		
		$scope.$watch("gridOptions.currentPage", function(){
			$scope.$emit("fetchPage", {service:coreService.Permission});
		});
		
		$scope.removeRow = function(row){
			$scope.$emit("removeRow", {service:coreService.Permission, row:row});
		};
		
	});
	
});

define(["core/module"], function(module){
	
	"use strict";
		
	module.registerController("userTableCtrl", function($scope, coreService){
		
		$scope.$watch("gridOptions.currentPage", function(){
			$scope.$emit("fetchPage", {service:coreService.User});
		});
		
		$scope.removeRow = function(row){
			$scope.$emit("removeRow", {service:coreService.User, row:row});
		};
		
	});
	
});

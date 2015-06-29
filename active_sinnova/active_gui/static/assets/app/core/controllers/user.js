define(["core/module"], function(module){
	
	"use strict";
		
	module.registerController("userCtrl", function($scope, coreService){
		
		$scope.getElement(coreService.User);
		
		$scope.$on("sidebarChanged", function(event, args){
			setGroups(args.selected);
			setPermissions(args.selected);
		});
		
		var setGroups = function (groups) {
			$scope.currentElement.groups = [];
			for(var i = 0; i < groups.length; i++) {
				if($scope.currentElement.groups.indexOf(groups[i].id) === -1){
					$scope.currentElement.groups.push(groups[i].id);
				}
			}
		};
		
		var setPermissions = function (groups){
			$scope.currentElement.user_permissions = [];
			for(var i = 0; i < groups.length; i++){
				if($scope.currentElement.groups.indexOf(groups[i].id) > -1){
					$scope.currentElement.user_permissions = copy_array($scope.currentElement.user_permissions, groups[i].permissions);
				}
			}
		};
		
		var copy_array = function(array1, array2) {
			for(var i = 0; i < array2.length; i++) {
				if(array1.indexOf(array2[i]) === -1){
					array1.push(array2[i]);
				}
			}
			return array1;
		};
		
	});
	
});

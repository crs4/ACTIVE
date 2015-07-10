define(["core/module"], function(module){
	
	"use strict";
		
	module.registerController("groupCtrl", function($scope, coreService){
		
		$scope.getElement(coreService.Group);
		
		$scope.$on("sidebarChanged", function(event, args){
			setPermissions(args.selected);
		});
		
		var setPermissions = function (permissions) {
			$scope.currentElement.permissions = [];
			for (var i = 0; i < permissions.length; i++) {
				if($scope.currentElement.permissions.indexOf(permissions[i].id) === -1)
					$scope.currentElement.permissions.push(permissions[i].id);
			}
		};
		
	});
	
});

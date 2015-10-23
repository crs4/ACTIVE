define(["core/module"], function(module){

	"use strict";

	module.registerController("audioInstanceCtrl", function($scope, Mediator){

		$scope.selectItems = function(items) {
			Mediator.mediateSelectedItems(items);
			$scope.$parent.selectedItems = items;
			$scope.currentItem = items[items.length - 1];
		};

	});

});

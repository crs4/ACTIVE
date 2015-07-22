define(["core/module", "appConfig"], function(module){
	
	"use strict";
		
	module.registerController("contextMenuCtrl", function($scope, $window, $document, $stateParams, $state, coreService){
		
		var menu   = $("div.context-menu");
		var active = "context-menu_active";
		
		$scope.selectedType = $stateParams.type;
		
		$window.onkeyup = function (event) {
			if (event.keyCode === 27) {
				menu.removeClass(active);
			}
		};
		
		$window.onresize = function (event) {
			menu.removeClass(active);
		};
		
		$document.onclick = function (event) {
			menu.removeClass(active);
		};

		$scope.$on("contextMenu", function(event, args){
			$scope.widgetContextModel = args.widgetContextModel;
		});

		$scope.deleteModel = function(){
			if($scope.widgetContextModel.id){
				coreService.Model.delete({"id":$scope.widgetContextModel.id}, function(){
					$state.reload();
				});
			}
		};

		$scope.deleteInstance = function(){
			if($scope.widgetContextModel.id){
				coreService.Instance.delete({"id":$scope.widgetContextModel.id}, function(){
					$state.reload();
				});
			}
		};
	
		$scope.buildModel = function(){
			if($scope.widgetContextModel.id){
				console.log("build model " + $scope.widgetContextModel.id);
			}
		};

		$scope.unbindInstance = function(){
			if($scope.widgetContextModel.id){
				$scope.widgetContextModel.entity_model = null;
				$scope.widgetContextModel.features = undefined;
				$scope.widgetContextModel.thumbnail = undefined;
				coreService.Instance.update({"id":$scope.widgetContextModel.id}, $scope.widgetContextModel, function(newElement){
					$state.reload();
				});
			}
		};
		
	});
	
});

define(["core/module", "humps", "mcustom-scrollbar"], function(module, humps){
	
	"use strict";
		
	module.registerController("scrollbarCtrl", function($scope, $element, $attrs, coreService, Mediator){
		
		$scope.scrollbarPage = 1;
		$scope.hasNextPage = true;
		$scope.selected = [];
		
		$scope.imChanged = function () {
			Mediator.mediateSidebarChange($scope.selected);
		};
		
		$scope.$on("elementReady", function(event, args){
			initScrollbar(args.element);
		});
		
		var myService = $attrs.scrollbarService;
		
		var initScrollbar = function(currentElement){
			$scope.elements = coreService[myService].query({page: $scope.scrollbarPage});
			$scope.elements.$promise.then(function (result) {
				$scope.elements = result.results;
				$element.mCustomScrollbar({
					theme: "rounded-dark",
					scrollInertia: 300,
					scrollEasing: "linear",
					scrollButtons: {
						enable: true
					},
					advanced: {
						updateOnContentResize: true
					},
					callbacks: {
						onTotalScroll: function() {
							next();
						},
						onUpdate: function() {
							if(angular.isDefined(currentElement.id)){
								var inner = getInner(currentElement);
								prepopulate(inner);
							}
						}
					}
				});
				if(result.next !== null){
					$scope.scrollbarPage += 1;
				} else {
					$scope.hasNextPage = false;
				}
			});
		};
		
		//TROVARE UNA SOLUZIONE MIGLIORE.
		var getInner = function(obj) {
			if(angular.isDefined(obj[myService.toLowerCase()]))
				return obj[myService.toLowerCase()];
			else if(angular.isDefined(obj[myService.toLowerCase()+ "s"]))
				return obj[myService.toLowerCase() + "s"];
			else if(angular.isDefined(obj[humps.decamelize(myService)]))
				return obj[humps.decamelize(myService)];
		};
		
		var prepopulate = function(list) {
			$scope.selected.length = 0;
			if(!angular.isArray(list)){
				for (var i = 0; i < $scope.elements.length; i++) {
					if ($scope.elements[i].id === list){
						$scope.selected.push($scope.elements[i].id);
						$scope.$apply();
					}
				}
			} else {
				for (var i = 0; i < $scope.elements.length; i++) {
					if (list.indexOf($scope.elements[i].id) > -1){
						$scope.selected.push($scope.elements[i]);
						$scope.$apply();
					}
				}
			}
		};
		
		var next = function () {
			if($scope.hasNextPage){
				var e = coreService[myService].query({page: $scope.scrollbarPage}, function(){
					$scope.elements = $scope.elements.concat(e.results);
					if(e.next !== null){
						$scope.scrollbarPage += 1;
					} else {
						$scope.hasNextPage = false;
					}
				});
			}
		};
		
	});
	
});

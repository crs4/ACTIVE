define(["core/module", "mcustom-scrollbar"], function(module){
	
	module.registerDirective("widgetScrollbar", function(coreService, Mediator){
		
		return {
			
            restrict: "A",
            templateUrl: "/assets/app/core/templates/scrollbar.html",
            controller: function ($scope, $element, $attrs) {
                $element.removeAttr("widget-scrollbar");
                
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
									if(angular.isDefined(currentElement.id))
										prepopulate(currentElement[myService.toLowerCase() + "s"]);//PROBLEMA: TROVARE NOME INNER LIST
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
				
				var test = function(obj, dirty_field) {
					Object.keys(obj);
				};
				
				var prepopulate = function(list) {
					$scope.selected.length = 0;
					for (var i = 0; i < $scope.elements.length; i++) {
						if (list.indexOf($scope.elements[i].id) > -1){
							$scope.selected.push($scope.elements[i]);
							$scope.$apply();
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
				
            }
            
        }
		
	});
	
});

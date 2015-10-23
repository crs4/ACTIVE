define(["layout/module"], function(module){

	module.registerController("peopleSearchCtrl", function($scope, $rootScope, $window, coreService, Mediator){
	
			$scope.scrollbarPage = 1;
			$scope.hasNextPage = true;
			$scope.elements = [];
			$scope.selected = [];
			
			$scope.$on("search_entity", function(event, args){
				reset();
				init(args);
			});
			
			/*$scope.doSearch = function(){
				var dict = {};
				dict = angular.copy($scope.context, dict);
				dict.filter_by.params.selected = $scope.selected;
				if(dict.filter_by.params.selected.length > 0)
					$rootScope.$broadcast("search_context", dict);
				$scope.closeModal();
			};*/

			$scope.$watchCollection("selected", function(newValue, oldValue){
				//Mediator.mediateEnableSummarizer(newValue);
				console.log(newValue);
				if(angular.isDefined(newValue) && newValue.length > 0)
					$window.open(appConfig.coreBaseUrl + "summarizer/" + newValue[0].id, "_blank");
			});

			angular.element("#search_modal").on("show.bs.modal", function(e){
				reset();
			});

			//HANDLERS
			
			var parseParams = function(params, page){
				var dict = {};
				for(var key in params)
					dict[key] = params[key];
				dict["page"] = page;
				return dict;
			};
			
			var init = function(context){
				var params = parseParams(context.filter_by.params, $scope.scrollbarPage);
				var p = coreService.Person.query(parseParams(params, $scope.scrollbarPage));
				p.$promise.then(function (result) {
					$scope.elements = result;
					angular.element("#search-entity").mCustomScrollbar({
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
								next(context);
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
			
			var next = function (context) {
				if($scope.hasNextPage){
					var params = parseParams(context.filter_by.params, $scope.scrollbarPage);
					var e = coreService.Person.query(params, function(){
						$scope.elements = $scope.elements.concat(e.results);
						if(e.next !== null){
							$scope.scrollbarPage += 1;
						} else {
							$scope.hasNextPage = false;
						}
					});
				}
			};

			var reset = function(){
				$scope.scrollbarPage = 1;
				$scope.hasNextPage = true;
				$scope.elements.length = 0;
				$scope.selected.length = 0;
			};
			
	});
	
});


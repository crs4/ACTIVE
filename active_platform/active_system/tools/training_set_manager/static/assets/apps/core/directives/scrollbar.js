define(["core/module", "mcustom-scrollbar"], function(module){

	"use strict";

	module.registerDirective("widgetScrollbar", function($state, $stateParams, Mediator, coreService){

		return {
			restrict: "A",
			scope: {
				scrollbarService: "@",
				scrollbarType: "@"
			},
			link: function(scope, element, attrs){
				element.removeAttr("widget-scrollbar");

				scope.elements = [];
				scope.scrollbarPage = 1;
				scope.hasNextPage = true;
				scope.selected = [];

				//FOR AUDIO INSTANCES ONLY - FORSE NON SERVE... CONTROLLARE BENE.
				scope.$watchCollection("elements", function(newValue, oldValue){
					if(scope.$parent.items){
						scope.$parent.items.length = 0;
						scope.$parent.items = newValue;
					}
				});

				scope.imChanged = function (params, checked) {
					Mediator.mediateScrollbarSelection(scope.selected);
				};

				var initScrollbar = function(){
					scope.elements = coreService[scope.scrollbarService].query(setQueryParams({page:scope.scrollbarPage}));
					scope.elements.$promise.then(function (result) {
						scope.elements = result.results;
						element.mCustomScrollbar({
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
								}
							}
						});
						if(result.next !== null){
							scope.scrollbarPage += 1;
						} else {
							scope.hasNextPage = false;
						}
					});
				};

				var next = function () {
					if(scope.hasNextPage){
						var e = coreService[scope.scrollbarService].query(setQueryParams({page:scope.scrollbarPage}), function(){
							scope.elements = scope.elements.concat(e.results);
							if(e.next !== null){
								scope.scrollbarPage += 1;
							} else {
								scope.hasNextPage = false;
							}
						});
					}
				};

				var setQueryParams = function(param_dict) {
					if($state.is("app.core.instances")){
						param_dict["type"] = $stateParams.type;
						param_dict["used"] = false;
					}
					return param_dict;
				};

				initScrollbar();

			},
			templateUrl: function(element, attribute){
				switch(element.attr("scrollbar-type")){
					case "radio": return "/static/assets/apps/core/templates/radio.html"; break;
					default: return "/static/assets/apps/core/templates/checkbox.html"; break;
				}
			}
		}

	});

});

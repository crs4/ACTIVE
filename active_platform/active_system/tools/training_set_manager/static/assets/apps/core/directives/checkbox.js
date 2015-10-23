define(["core/module"], function(module){
	
	"use strict";
		
	module.registerDirective("widgetCheckbox", function(){
		
		return {
			restrict: "A",
			templateUrl: "/assets/apps/core/templates/checkbox.html",
			link: function(scope, element, attributes){
				element.removeAttr("widget-checkbox");
			}
		}
		
	});
	
});


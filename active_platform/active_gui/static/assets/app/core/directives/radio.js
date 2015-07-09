define(["core/module"], function(module){
	
	module.registerDirective("widgetRadio", function(){
		
		return {
			
            restrict: "A",
            templateUrl: "/assets/app/core/templates/radio.html",
            link: function (scope, element, attributes) {
                element.removeAttr("widget-radio");
            }
            
        }
		
	});
	
});

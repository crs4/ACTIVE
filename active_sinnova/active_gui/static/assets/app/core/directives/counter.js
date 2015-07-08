define(["core/module"], function (module) {

    "use strict";

    module.registerDirective("widgetCounter", function ($compile) {
		
        return {
			
            restrict: "A",
            templateUrl: "/assets/app/core/templates/counter.html",
            link: function (scope, element) {
                element.removeAttr("widget-counter");
            }
        }
        
    });

});



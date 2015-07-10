define(["core/module"], function (module) {

    "use strict";

    module.registerDirective("widgetSelect", function ($compile) {
		
        return {
			
            restrict: "A",
            templateUrl: "/assets/app/core/templates/select.html",
            link: function (scope, element) {
                element.removeAttr("widget-select");
            }
        }
        
    });

});



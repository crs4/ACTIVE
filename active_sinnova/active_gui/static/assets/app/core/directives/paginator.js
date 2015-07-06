define(["core/module"], function (module) {

    "use strict";

    module.registerDirective("widgetPaginator", function ($compile) {
		
        return {
			
            restrict: "A",
            templateUrl: "/assets/app/core/templates/paginator.html",
            link: function (scope, element, attributes) {
                element.removeAttr("widget-paginator");
            }
            
        }
        
    });

});



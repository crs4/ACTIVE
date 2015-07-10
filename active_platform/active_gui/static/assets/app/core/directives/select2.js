define(["core/module", "select2"], function (module) {

    "use strict";

    module.registerDirective("widgetSelect2", function ($compile) {
		
        return {
			restrict: "A",
			templateUrl: "/assets/app/core/templates/select2.html",
			compile: function (element, attributes) {
				element.removeAttr("widget-select2");
				element.find("#s2").select2({placeholder:"Actions"});
			}
		}
        
    });

});



define(["layout/module", "theme"], function (module, Theme) {

    "use strict";

    module.registerDirective("settingAside", function () {
		
        return {
            restrict: "A",
            link: function (scope, element) {
                element.removeAttr("setting-aside");
				Theme.tree();
            }
        }
        
    });

});




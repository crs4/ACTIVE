define(["layout/module", "theme"], function (module, Theme) {

    "use strict";

    module.registerDirective("settingHeader", function () {
		
		return {
			restrict: "A",
			link: function(scope, element){
				element.removeAttr("setting-header");
				
				//Activate sidebar push menu
				if (Theme.options.sidebarPushMenu) {
					Theme.pushMenu(Theme.options.sidebarToggleSelector);
				}
				
			}
		}
		
    });
});

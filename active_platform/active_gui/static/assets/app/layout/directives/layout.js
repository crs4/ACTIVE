define(["layout/module", "theme"], function (module, Theme) {

    "use strict";

    module.registerDirective("settingLayout", function () {
		
		return {
			restrict: "A",
			link: function(scope, element){
				element.removeAttr("setting-layout");
				
				Theme.layout.activate();
				
				//Activate Bootstrap tooltip
				if (Theme.options.enableBSToppltip) {
					$(Theme.options.BSTooltipSelector).tooltip();
				}
				
				// INITIALIZE BUTTON TOGGLE
				$('.btn-group[data-toggle="btn-toggle"]').each(function () {
					var group = $(this);
					$(this).find(".btn").click(function (e) {
						group.find(".btn.active").removeClass("active");
						$(this).addClass("active");
						e.preventDefault();
					});
				});
				
			}
		}
		
    });
});

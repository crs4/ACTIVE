define(["core/module"], function (module) {

    "use strict";

    module.registerDirective("widgetViewer", function ($compile, viewerService) {
        return {
            restrict: "A",
            templateUrl: "/assets/app/core/templates/media_image.html",
            link: function (scope, element) {
                
				var galleryElements = angular.element.find(".my_gallery");

				for(var i = 0, l = galleryElements.length; i < l; i++) {
					galleryElements[i].setAttribute("data-pswp-uid", i+1);
					galleryElements[i].onclick = viewerService[0];
				}

				var hashData = viewerService[1]();
				
				if(hashData.pid > 0 && hashData.gid > 0) {
					viewerService[2](hashData.pid - 1 ,  galleryElements[ hashData.gid - 1 ], true );
				}

            }
        }
    });

});

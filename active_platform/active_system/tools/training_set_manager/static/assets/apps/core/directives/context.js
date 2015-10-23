define(["core/module"], function(module){
	
	"use strict";
	
	module.registerDirective("widgetContext", function($compile, $window, $document, Mediator){
		
		return {
			
			restrict: "A",
			require: "preloadFile",
			link: function (scope, element, attributes, preloadFileCtrl) {
				element.removeAttr("widget-context");
				
				var menu   = $("div.context-menu");
				var active = "context-menu_active";
				
				var clickCoords;
				var clickCoordsX;
				var clickCoordsY;
				
				var menuWidth;
				var menuHeight;
				
				var windowWidth;
				var windowHeight;
				
				var getPosition = function(event){
					var _x = 0;
					var _y = 0;
					
					if (event.pageX || event.pageY) {
						_x = event.pageX;
						_y = event.pageY;
					} else if (event.clientX || event.clientY) {
						_x = event.clientX + $document.body.scrollLeft + 
										   $document.documentElement.scrollLeft;
						_y = event.clientY + $document.body.scrollTop + 
										   $document.documentElement.scrollTop;
					}

					return {
						x: _x,
						y: _y
					}
				};
				
				var positionMenu = function(event) {
					clickCoords = getPosition(event);
					clickCoordsX = clickCoords.x;
					clickCoordsY = clickCoords.y;
					
					menuWidth = menu.prop("offsetWidth") + 4;
					menuHeight = menu.prop("offsetHeight") + 4;

					windowWidth = $window.innerWidth;
					//windowHeight = $window.innerHeight;
					windowHeight = document.body.scrollHeight;
					
					if ((windowWidth - clickCoordsX) < menuWidth) {
						var p = windowWidth - menuWidth + "px";
						menu.css("left", p);
					} else {
						var p = clickCoordsX + "px";
						menu.css("left", p);
					}
					
					if ((windowHeight - clickCoordsY) < menuHeight) {
						var p = windowHeight - menuHeight + "px";
						menu.css("top", p);
					} else {
						var p = clickCoordsY + "px";
						menu.css("top", p);
					}
				};
				
				element.on("contextmenu", function (event) {
					event.preventDefault();
					menu.addClass(active);
					positionMenu(event);
					Mediator.mediateContextMenuEvent(preloadFileCtrl.getItem());
				});
				
			}
			
		}
		
	});
	
});

define(["core/module", "appConfig", "editable"], function(module){

	"use strict";

	module.registerDirective("widgetEditable", function(coreService){

		return {
			restrict: "A",
			scope: {
				editableItem: "="
			},
			link: function(scope, element, attributes){
				element.removeAttr("widget-editable");
				element.editable({
					type: "text",
					pk: scope.editableItem.id,
					value: scope.editableItem.name,
					title: "Edit model name",
					url: function(params){
						scope.editableItem.name = params.value;
						scope.editableItem.model_file = undefined;
						coreService.Model.update({"id":params.pk}, scope.editableItem, function(){
							angular.noop();
						});
					}
				});
			}
		}

	});

});

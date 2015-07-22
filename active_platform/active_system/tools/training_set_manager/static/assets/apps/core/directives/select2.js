define(["core/module", "appConfig", "select2"], function (module) {

    "use strict";

    module.registerDirective("widgetSelect2", function ($compile, $stateParams) {
	
	function formatRepo(line){
		if (!line.id) { return line.name; }
		var $line = $('<span>' + line.id + ' - ' + line.name + '</span>');
		return $line;
	};
	
        return {
			restrict: "A",
			//templateUrl: "/static/assets/apps/core/templates/select2.html",
			link: function (scope, element, attributes) {
				element.removeAttr("widget-select2");
				$(".select2").select2({
					placeholder:"Models",
					ajax: {
						url: appConfig.apiUrl + "models/?type=" + $stateParams.type,
						dataType: "json",
    						delay: 250,
						data: function (params) {
							return {
								q: params.term,
								page: params.page
							};
						},
						processResults: function (data, page) {
							return {
								results: data.results
							};
						}
					},
					cache: true,
					escapeMarkup: function (markup) { return markup; },
					minimumInputLength: 3,
					templateResult: formatRepo
				});
				//element.find("#s2").select2({placeholder:"Actions"});
			}
		}
        
    });

});



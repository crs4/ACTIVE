define(["core/module", "appConfig", "select2"], function (module) {

    "use strict";

    module.registerDirective("widgetSelect2", function ($compile, $stateParams) {
	
	function formatResult(line){
		if (!line.id) { return line.name; }
		var $line = $("<span>" + line.id + " - " + line.name + "</span>");
		return $line;
	};
	
        return {
			restrict: "A",
			link: function (scope, element, attributes) {
				element.removeAttr("widget-select2");
				$(".select2").select2({
					placeholder: "Models",
					theme: "bootstrap",
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
						processResults: function (data, params) {
							params.page = params.page || 1;
							return {
								results: data.results,
								pagination: {
									more: (params.page * appConfig.pageSize) < data.count
								}
							};
						},
						cache: true
					},
					escapeMarkup: function (markup) { return markup; },
					minimumInputLength: 3,
					templateResult: formatResult
				});
			}
		}
        
    });

});



define(["core/module", "dropzone", "appConfig"], function (module) {

    "use strict";

    module.registerDirective("widgetDropzone", function ($compile, $localStorage) {
		
        return {
			
            restrict: "AE",
            link: function (scope, element) {
                element.removeAttr("widget-dropzone");
                
				var myDropzone = new Dropzone("#dropzone", {
					url: function(file){
						return appConfig.coreApiUrl + "items/" + file[0].type.split("/")[0] + "/";
					},
					parallelUploads: 10,
					maxFilesize: 10000
				});
				
				myDropzone.on("sending", function(file, xhr, formData){
					if($localStorage.token)
						xhr.setRequestHeader("Authorization", "Bearer " + $localStorage.token.access_token);
					formData.append("filename", file.name);
					formData.append("filesize", file.size);
					formData.append("type", file.type.split("/")[0]);
					formData.append("format", file.type.split("/")[1]);
					formData.append("owner", 1);
					formData.append("visibility", false);
				});

            }
        }
        
    });

});



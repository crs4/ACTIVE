var require = {
	
    	waitSeconds: 0,

    	paths: {
		"jquery": "../plugins/jQuery/jQuery-2.1.3.min",
		"slimscroll": "../plugins/slimScroll/jquery.slimscroll.min",
		"bootstrap": "../bootstrap/js/bootstrap.min",
		"angular":"../plugins/angular/angular.min",
		"angular-resource": "../plugins/angular/angular-resource.min",
		"angular-cookies": "../plugins/angular/angular-cookies.min",
		"angular-sanitize": "../plugins/angular/angular-sanitize.min",
		"angular-couch-potato": "../plugins/angular-couch-potato/dist/angular-couch-potato",
		"angular-ui-router": "../plugins/angular-ui-router/release/angular-ui-router.min",
		"ng-infinite-scroll": "../plugins/scroll/ng-infinite-scroll.min",
		"videogular": "../plugins/videogular/videogular.min",
		"vg-controls": "../plugins/videogular/vg-controls.min",
		"vg-poster": "../plugins/videogular/vg-poster.min",
		"editable": "../plugins/angular-xeditable/bootstrap-editable.min",
		"checklist-model": "../plugins/checklist-model/checklist-model",
		"domReady": "../plugins/requirejs-domready/domReady",
		"select2": "../plugins/select2/select2.min",
		"mcustom-scrollbar": "../plugins/mcustom-scrollbar/jquery.mCustomScrollbar.concat.min",
		"appConfig": "../app.config",
		"theme": "../theme/js/theme"
	},
    	shim: {
		"bootstrap": { deps: ["jquery"] },
		"angular": {"exports": "angular", deps: ["jquery"] },
		"angular-resource": { deps: ["angular"] },
		"angular-cookies": { deps: ["angular"] },
		"angular-sanitize": { deps: ["angular"] },
		"angular-ui-router": { deps: ["angular"] },
		"angular-couch-potato": { deps: ["angular"] },
		"ng-infinite-scroll": { deps: ["angular"] },
		"videogular": { deps: ["angular"] },
       		"vg-controls": { deps: ["angular"] },
		"vg-poster": { deps: ["angular"] },
		"checklist-model": {  deps: ["angular"] },
		"slimscroll": { deps: ["jquery"] },
		"select2": { deps: ["jquery"] },
		"mcustom-scrollbar": { deps: ["jquery"] },
		"theme": { deps: ["jquery", "slimscroll"]}
	},
	priority: [
		"jquery",
		"bootstrap",
		"angular"
    	]
	
};


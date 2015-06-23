"use strict";

var appConfig = {};

appConfig.coreBaseUrl = "http://localhost:80/";
appConfig.jobmonitorBaseUrl = "http://localhost:80/jobmonitor/";

appConfig.coreApiUrl = appConfig.coreBaseUrl + "api/";
appConfig.userApiUrl = appConfig.coreBaseUrl + "api/users/";
appConfig.jobApiUrl = appConfig.jobmonitorBaseUrl;
appConfig.nodeApiUrl = appConfig.jobmonitorBaseUrl + "cluster/";

appConfig.itemPageSize = 32;
appConfig.tablePageSize = 10;

appConfig.checkPages = function(items_length, pageSize){
	var pagesBefore = Math.ceil(items_length + 1, pageSize);
	var pagesAfter  = Math.ceil(items_length, pageSize);
	if(pagesAfter < pagesBefore)
		return -1;
	return 0;
};

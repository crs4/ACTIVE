"use strict";

var appConfig = {};

appConfig.coreBaseUrl = "http://156.148.132.79:80/";
appConfig.jobmonitorBaseUrl = "http://156.148.132.79:80/job_monitor/";

//appConfig.coreBaseUrl = "http://localhost:4000/";
//appConfig.jobmonitorBaseUrl = "http://localhost:4000/job_monitor/";

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

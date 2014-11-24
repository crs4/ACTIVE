// Initialize all required objects.
var http = require("http");
var fs = require("fs");
var path = require("path");
var url = require('url');

// Give the initial folder. Change the location to whatever you want.
var initFolder = '/home/sviluppo/nodejs/ACTIVE/video_summarizer';

// List filename extensions and MIME names we need as a dictionary. 
var mimeNames = {
    '.css': 'text/css',
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.mp3': 'audio/mpeg',
    '.mp4': 'video/mp4',
    '.mov': 'video/mp4',
    '.ogg': 'application/ogg', 
    '.ogv': 'video/ogg', 
    '.oga': 'audio/ogg',
    '.txt': 'text/plain',
    '.wav': 'audio/x-wav',
    '.webm': 'video/webm'
};

http.createServer(httpListener).listen(8000, '0.0.0.0');

function httpListener(request, response) {
    // We will only accept 'GET' method. Otherwise will return 405 'Method Not Allowed'.
    if (request.method != 'GET') {
        sendResponse(response, 405, { 'Allow': 'GET' }, null);
        return null;
    }

    var filename =
        initFolder + url.parse(request.url, true, true).pathname.split('/').join(path.sep);

    // Check if file exists. If not, will return the 404 'Not Found'. 
    if (!fs.existsSync(filename)) {
        sendResponse(response, 404, null, null);
        return null;
    }

    var responseHeaders = {};
    var stat = fs.statSync(filename);
    var rangeRequest = readRangeHeader(request.headers['range'], stat.size);

    // If 'Range' header exists, we will parse it with Regular Expression.
    if (rangeRequest == null) {
        responseHeaders['Content-Type'] = getMimeNameFromExt(path.extname(filename));
        responseHeaders['Content-Length'] = stat.size;  // File size.
        responseHeaders['Accept-Ranges'] = 'bytes';

        //  If not, will return file directly.
        sendResponse(response, 200, responseHeaders, fs.createReadStream(filename));
        return null;
    }

    var start = rangeRequest.Start;
    var end = rangeRequest.End;

    // If the range can't be fulfilled. 
    if (start >= stat.size || end >= stat.size) {
        // Indicate the acceptable range.
        responseHeaders['Content-Range'] = 'bytes */' + stat.size; // File size.

        // Return the 416 'Requested Range Not Satisfiable'.
        sendResponse(response, 416, responseHeaders, null);
        return null;
    }

    // Indicate the current range. 
    responseHeaders['Content-Range'] = 'bytes ' + start + '-' + end + '/' + stat.size;
    responseHeaders['Content-Length'] = start == end ? 0 : (end - start + 1);
    responseHeaders['Content-Type'] = getMimeNameFromExt(path.extname(filename));
    responseHeaders['Accept-Ranges'] = 'bytes';
    responseHeaders['Cache-Control'] = 'no-cache';

    // Return the 206 'Partial Content'.
    sendResponse(response, 206, 
        responseHeaders, fs.createReadStream(filename, { start: start, end: end }));
}

function sendResponse(response, responseStatus, responseHeaders, readable) {
    response.writeHead(responseStatus, responseHeaders);

    if (readable == null)
        response.end();
    else
        readable.on('open', function () {
            readable.pipe(response);
        });

    return null;
}

function getMimeNameFromExt(ext) {
    var result = mimeNames[ext.toLowerCase()];
    
    // It's better to give a default value.
    if (result == null)
        result = 'application/octet-stream';
    
    return result;
}

function readRangeHeader(range, totalLength) {
        /*
         * Example of the method 'split' with regular expression.
         * 
         * Input: bytes=100-200
         * Output: [null, 100, 200, null]
         * 
         * Input: bytes=-200
         * Output: [null, null, 200, null]
         */

    if (range == null || range.length == 0)
        return null;

    var array = range.split(/bytes=([0-9]*)-([0-9]*)/);
    var start = parseInt(array[1]);
    var end = parseInt(array[2]);
    var result = {
        Start: isNaN(start) ? 0 : start,
        End: isNaN(end) ? (totalLength - 1) : end
    };
    
    if (!isNaN(start) && isNaN(end)) {
        result.Start = start;
        result.End = totalLength - 1;
    }

    if (isNaN(start) && !isNaN(end)) {
        result.Start = totalLength - end;
        result.End = totalLength - 1;
    }

    return result;
}




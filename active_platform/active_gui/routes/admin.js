var express = require('express');

var router = express.Router();

router.get('/private', function(req, res){
	res.render('admin');
});

router.get('/private/jobmonitor', function(req, res){
	res.render('jobmonitor');
});

module.exports = router;

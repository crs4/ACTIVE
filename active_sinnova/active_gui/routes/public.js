var express = require('express');

var router = express.Router();

router.get('/', function(req, res){
	res.render('index');
});

router.get('/jobmonitor', function(req, res){
	res.render('jobmonitor');
});

router.get('/consumer/exchange', function(req, res){
	res.render('exchange');
});

module.exports = router;

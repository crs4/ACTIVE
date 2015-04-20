var express = require('express');
var morgan = require('morgan');
var bodyParser = require('body-parser');
var methodOverride = require('method-override');
var public = require('./routes/public');
var admin = require('./routes/admin');

var app = express();

app.set('view engine', 'ejs');

app.use(express.static(__dirname + '/static'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(morgan('dev'));
app.use(methodOverride());

app.use('/', public);
app.use('/admin', admin);

app.listen(3000, function(){
	console.log("** SERVER LISTEN ON PORT 3000.");
});


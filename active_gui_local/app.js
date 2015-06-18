var express = require('express');
var morgan = require('morgan');
var bodyParser = require('body-parser');
var methodOverride = require('method-override');
var modRewrite = require("connect-modrewrite");
var public = require('./routes/public');
var admin = require('./routes/admin');

var app = express();

app.set('view engine', 'ejs');

app.use(express.static(__dirname + '/static'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(morgan('dev'));
app.use(methodOverride());

app.use(modRewrite([
	"^/users$ /",
	"^/users/\\d*$ /",
	"^/groups$ /",
	"^/groups/\\d*$ /",
	"^/permissions$ /",
	"^/permissions/\\d*$ /",
	"^/upload$ /",
	"^/items/image$ /",
	"^/items/video$ /",
	"^/items/audio$ /",
	"^/error/\\w*$ /"
]));

app.use('/', public);
app.use('/admin', admin);

app.listen(4000, function(){
	console.log("** SERVER LISTEN ON PORT 4000.");
});


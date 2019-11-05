// By: Matt Penny
// Originally made for COMP 3005 winter 2016 class
// Slightly gutted, and modified to be vulnerable to SQLi

var bodyParser = require('body-parser');
var express = require('express');
var path = require('path');
var url = require('url');
var sqlite = require('sqlite3');

var port = process.env.PORT || 3000;
var app = express();

// We don't want people deleting the flag
var db = new sqlite.Database('phone.db', sqlite.OPEN_READONLY);

/* App routes */
var routes = require('./routes/ui')(db);

app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(express.static(path.join(__dirname, 'public')));

/*app.locals.pretty = true;*/
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use('/', routes);

app.listen(port, function() {
    console.log(`Listening on port ${port}`);
});

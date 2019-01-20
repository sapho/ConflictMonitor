let express = require('express');
let path = require('path');
let logger = require('morgan');
// let cookieParser = require('cookie-parser');
let bodyParser = require('body-parser');


let app = express();
/* give access to following folders */
app.use(express.static("../server"));
app.use(express.static("../app"));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
//app.use(express.static(""));  //hier Pfad zu metadaten einfügen
app.use(logger('combined'));

/* http routing. */
// log code which is executed on every request
app.use(function (req, res, next) {
    console.log(req.method + ' ' + req.url + ' was requested by ' + req.connection.remoteAddress);
    res.header('Access-Control-Allow-Origin', '*'); // allow CORS
    next();
});

app.use(function (req, res, next) {
    let err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handler
app.use(function (err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};
    // render the error page
    res.status(err.status || 500);
    res.send('Error Status 500');
});


module.exports = app;

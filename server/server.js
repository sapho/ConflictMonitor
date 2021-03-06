/**
 * Module dependencies.
 */

let app = require('./app');
let debug = require('debug')('stml:server');
let http = require('http');
let callScripts = require ('./callscripts');
let dockerCmdJs = require('docker-cmd-js');
let cmd = new dockerCmdJs.Cmd();

/**
 * Get port from environment and store in Express.
 */

let port = normalizePort(process.env.PORT || '8080');
app.set('port', port, 'Content-Type', 'application/json');

/**
 * Create HTTP server.
 */
let server = http.createServer(app);

cmd.debug().run('docker build --no-cache -t basti_ac -f ../pre_processing/atmospheric_correction/Dockerfile .')
    .then(() => cmd.run('docker build --no-cache -t basti_c -f ../pre_processing/composites/Dockerfile .'))
    .then(function(){
        startServer();
    })
    .catch((err) => console.error(err));


function startServer(){
    /**
     * Listen on provided port, on all network interfaces.
     */

    server.listen(port);
    server.on('error', onError);
    server.on('listening', onListening);
}

/**
 * Normalize a port into a number, string, or false.
 */

function normalizePort(val) {
    let port = parseInt(val, 10);

    if (isNaN(port)) {
        // named pipe
        return val;
    }

    if (port >= 0) {
        // port number
        return port;
    }

    return false;
}

/**
 * Event listener for HTTP server "error" event.
 */
//sudo docker run -p 8080:8080 niklas/node-web-app
function onError(error) {
    if (error.syscall !== 'listen') {
        throw error;
    }

    let bind = typeof port === 'string'
        ? 'Pipe ' + port
        : 'Port ' + port;

    // handle specific listen errors with messages
    switch (error.code) {
        case 'EACCES':
            console.error(bind + ' requires elevated privileges');
            process.exit(1);
            break;
        case 'EADDRINUSE':
            console.error(bind + ' is already in use');
            process.exit(1);
            break;
        default:
            throw error;
    }
}

/**
 * Event listener for HTTP server "listening" event.
 */

function onListening() {
    let addr = server.address();
    let bind = typeof addr === 'string'
        ? 'pipe ' + addr
        : 'port ' + addr.port;
    debug('Listening on ' + bind);

    console.log('Server listening on Port ' + addr.port);

    //call Scripts when everything is in its place
    // callScripts.request();
}
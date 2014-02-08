var http = require('http')
    , path = require('path')
    , connect = require('connect')
    , express = require('express')
    , app = express();

var cookieParser = express.cookieParser('your secret sauce')
    , sessionStore = new connect.middleware.session.MemoryStore();

app.configure(function () {
    app.set('views', path.resolve('views'));
    app.set('view engine', 'jade');

    app.use(express.bodyParser());
    app.use(express.methodOverride());
    app.use(cookieParser);
    app.use(express.session({ store: sessionStore }));
    app.use(app.router);
});

var server = http.createServer(app)
    , io = require('socket.io').listen(server);

var SessionSockets = require('session.socket.io')
    , sessionSockets = new SessionSockets(io, sessionStore, cookieParser);

app.get('/', function (req, res) {
    req.session.foo = req.session.foo || 'bar';
    res.render('index');
});

sessionSockets.on('connection', function (err, socket, session) {
    socket.emit('session', session);
    socket.on('foo', function (value) {
        session.foo = value;
        session.save();
        socket.emit('session', session);
    });
});

server.listen(8001);

/*
 function sendMessage(channel, req, res, next){
 res.header("Access-Control-Allow-Origin", "*");
 res.header("Access-Control-Allow-Headers", "X-Requested-With");

 if (req.params.message === undefined) {
 return next(new restify.InvalidArgumentError('Message missing from request'))
 } else {
 util.log(req.params.message);
 //notify subscribers of data
 io.sockets.emit(channel, req.params);

 //return success to caller
 res.json({result: req.params.message});
 }
 return next();

 };

 server.use(restify.bodyParser());
 server.post('/api/activity', function (req, res, next) {
 sendMessage('activity', req, res, next);
 });

 server.post('/api/notification', function (req, res, next) {
 console.log("Notification received");
 sendMessage('notification', req, res, next);
 });

 */

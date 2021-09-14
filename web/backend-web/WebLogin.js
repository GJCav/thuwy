const SocketIO = require('socket.io');
const random = require('string-random');
const express = require('express');
const qr = require('qr-image');

var clients = {};

function clean() {
  for (let key in clients) {
    if (clients[key].disconnected) {
      delete clients[key];
    }
  }
}

async function main(server, app) {
  const io = SocketIO(server, {
    cors: {
      origin: "*"
    }
  });

  io.on('connection', socket => {
    socket.id = random(16);
    console.log('connected, ID: %s', socket.id);
    clients[socket.id] = socket;
    socket.on('disconnect', () => {
      delete clients[socket.id];
      console.log('disconnected, online: %d', Object.keys(clients).length);
    });

    socket.on('getRequestId', () => {
      socket.emit('requestId', socket.id);
    });

    console.log('connected, online: %d', Object.keys(clients).length);
  });

  app.post('/weblogin', express.json(), (req, res) => {
    let requestId = req.body['requestId'] || '';
    let credential = req.body['credential'] || '';
    clean();
    res.status(200);
    if (clients.hasOwnProperty(requestId)) {
      clients[requestId].emit('credential', credential);
      res.json({
        code: 0,
        msg: 'OK'
      }).end();
    } else {
      res.json({
        code: 400,
        msg: 'Request ID Invalid'
      }).end();
    }
  });

  app.get('/qr/:text', (req, res) => {
    let text = req.params.text;
    res.header({
      'Content-Type': 'image/png'
    });
    qr.image(text, { size: 10 }).pipe(res);
  });

  console.log('WebLogin setup done');

  let cleaner = setInterval(clean, 10000);
}

module.exports = main;
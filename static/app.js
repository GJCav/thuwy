const express = require('express');
const { Client } = require('minio');
const config = require('./config');

const client = new Client({
    endPoint: config.endPoint,
    port: config.endPointPort,
    useSSL: false,
    accessKey: config.accessKey,
    secretKey: config.secretKey
});

const app = express();

function PresignedPutObject(bucket, filename) {
    return new Promise((resolve, reject) => {
        try {
            client.presignedPutObject(bucket, filename, (err, url) => {
                if (err) {
                    reject(err);
                    return;
                }
                resolve(url);
            });
        } catch (err) {
            reject(err);
        }
    });
}

function makeDate() {
    const myDate = new Date();
    return `${myDate.getFullYear()}/${myDate.getMonth() < 9 ? ('0' + (myDate.getMonth() + 1)) : (myDate.getMonth() + 1)}/${myDate.getDate()}`;
}

app.get(['/uploadurl/:name', '/uploadurl'], async (req, res) => {
    let filename = `${makeDate()}/${Date.now()}_${req.params.name || 'unamed.bin'}`;
    console.log('filename: %s', filename);
    try {
        let url = await PresignedPutObject(config.targetBucket, filename);
        console.log('url: %s\n', url);
        res.end(url);
    } catch (err) {
        console.error(err);
        res.status(500).end();
    }
});

app.get('/', express.static(__dirname + '/demo'));

app.listen(config.listenPort, () => {
    console.log('wy-rsv static server is listening at %d', config.listenPort);
});

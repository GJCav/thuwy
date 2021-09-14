require('dotenv').config();
const express = require('express');
const http = require('http');
const { Client } = require('minio');
const config = require('./config');
const multer = require('multer');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const WebLoginSetup = require('./WebLogin');

app.use(cors({
    credentials: true,
    origin: config.frontendOrigin
}));

WebLoginSetup(server, app);

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, '/tmp')
    },
    filename: function (req, file, cb) {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9)
        cb(null, file.fieldname + '-' + uniqueSuffix)
    }
});

const upload = multer({ storage: storage });

const client = new Client({
    endPoint: config.endPoint,
    port: config.endPointPort,
    useSSL: true,
    accessKey: config.accessKey,
    secretKey: config.secretKey
});

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
        res.status(200).json({
            code: 0,
            msg: 'OK',
            data: url
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({
            code: 500,
            msg: 'failed',
            data: url
        });
    }
});

app.post(['/upload/:name', '/upload'], upload.single('file'), async (req, res) => {
    console.log(req.file);
    const { originalname, path, mimetype } = req.file;
    const filename = `${makeDate()}/${Date.now()}_${req.params.name || originalname || 'unamed.bin'}`;
    try {
        let res = await client.fPutObject(config.targetBucket, filename, path, {
            'Content-Type': mimetype
        });
        console.log(res);
    } catch (e) {
        console.error(e);
        res.status(500).json({
            code: 500,
            msg: 'failed'
        });
        return;
    }
    res.status(200).json({
        code: 0,
        msg: 'OK',
        data: `https://${config.endPoint}/${config.targetBucket}/${filename}`
    });
});

app.get('/', express.static(__dirname + '/demo'));

server.listen(config.listenPort, () => {
    console.log('wy-rsv static server is listening at %d', config.listenPort);
});

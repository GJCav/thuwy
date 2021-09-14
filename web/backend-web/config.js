module.exports = {
    endPoint: process.env.ENDPOINT,
    endPointPort: Number(process.env.ENDPOINT_PORT),
    frontendOrigin: process.env.FRONTEND_ORIGIN,
    targetBucket: process.env.BUCKET,
    accessKey: process.env.ACCESS_KEY,
    secretKey: process.env.SECRET_KEY,
    listenPort: Number(process.env.PORT),
}
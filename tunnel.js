const localtunnel = require('localtunnel'),
      fs = require('fs');

const port = process.argv[2];
localtunnel(port)
    .then(tunnel => { fs.writeFileSync("/tmp/url", tunnel.url) })
    .catch(e => console.error(e))
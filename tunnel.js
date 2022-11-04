const localtunnel = require('localtunnel'),
      fs = require('fs');

const port = sys.argv[2]
localtunnel(sys.argv[2])
    .then(tunnel => { fs.writeFileSync("/tmp/url", tunnel.url) })
    .catch(e => console.error(e))
const localtunnel = require('localtunnel'),
      fs = require('fs');

const port = process.argv[2];
const tunnel_dir = process.argv[3];
localtunnel(port)
    .then(tunnel => {
        try { fs.mkdirSync(tunnel_dir); }
        catch (e) { if (e.code !== 'EEXIST') throw e; }

        fs.writeFileSync(tunnel_dir + "/url", tunnel.url);
        const socket_url = tunnel.url.replace("https://", "wss://") + "/ws";
        fs.writeFileSync(tunnel_dir + "/socket.js", `socket_url = "${socket_url}";`);
    })
    .catch(e => console.error(e));
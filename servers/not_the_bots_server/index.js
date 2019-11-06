// config
const HOST_PORT = 3000;
const FLAG = 'flag{r0b0ts_d0t_txt_1s_n0t_s3cur1ty}';

const express = require('express');
const helmet = require('helmet');
const app = express();
app.listen(HOST_PORT);

app.get('/', (req, res) => {
  res.sendFile(__dirname+'/home.html');
});

app.get('/robots.txt', (req, res) => {
  const userAgent = req.headers['user-agent'];
  if(userAgent.indexOf('Googlebot')>-1){
    res.sendFile(__dirname+'/robots.txt');
  }else{
    res.sendStatus(401);
  }
});

app.get('/flag-e344db6c4d829be348157715b2658ce5d18a659f', (req, res) => {
  res.send(`${FLAG} <p> You should not rely on obfuscating robots.txt for security.`);
});

app.get('/*', (req, res) => {
    res.sendStatus(404);
});
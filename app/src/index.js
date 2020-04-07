const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const mysql = require('mysql');
const events = require('./events');
const connection = mysql.createConnection({
  host     : 'airqualitydatabaseinstance.chjnq0teubeh.eu-west-1.rds.amazonaws.com',
  user     : 'admin',
  password : 'myname18',
  database : 'airqualitydatabase'
});
connection.connect();
const port = process.env.PORT || 8080;
const app = express()
  .use(cors())
  .use(bodyParser.json())
  .use(events(connection));
app.listen(port, () => {
  console.log(`Express server listening on port ${port}`);
});

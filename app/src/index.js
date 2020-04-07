
connection.connect();
const port = process.env.PORT || 8080;
const app = express()
  .use(cors())
  .use(bodyParser.json())
  .use(events(connection));
app.listen(port, () => {
  console.log(`Express server listening on port ${port}`);
});

const express = require('express');
function createRouter(db) {
  const router = express.Router();
  const owner = '';



router.get('/query1', function (req, res, next) {
  db.query(
    'SELECT date, time, average_no2 FROM airquality WHERE average_no2 > 18 ORDER BY date',
    [owner, 10*(req.params.page || 0)],
    (error, results) => {
      if (error) {
        console.log(error);
        res.status(500).json({status: 'error'});
      } else {
        res.status(200).json(results);
      }
    }
  );
});

router.get('/query2', function (req, res, next) {
  db.query(
    'SELECT count(date) FROM airquality WHERE average_no2 > 18',
    [owner, 10*(req.params.page || 0)],
    (error, results) => {
      if (error) {
        console.log(error);
        res.status(500).json({status: 'error'});
      } else {
        res.status(200).json(results);
      }
    }
  );
});


router.get('/query3', function (req, res, next) {
  db.query(
    'SELECT date, time, co, tin_oxide, metanic_hydro,benzene_conc, titania, nox, tungsten_oxide_nox, average_no2, tungsten_oxide_no2,indium_oxide,temp,relative_humidity,absolute_humidity FROM airquality WHERE average_no2 > 18 ORDER BY date',
    [owner, 10*(req.params.page || 0)],
    (error, results) => {
      if (error) {
        console.log(error);
        res.status(500).json({status: 'error'});
      } else {
        res.status(200).json(results);
      }
    }
  );
});


  return router;
}
module.exports = createRouter;

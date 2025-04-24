const express = require('express');
const router = express.Router();
const path = require('path');

const fetch = require('node-fetch');



router.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../../../frontend/landing.html'));
});

module.exports = router;

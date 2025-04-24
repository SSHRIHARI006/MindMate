const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');

// Load env variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(cors());

// Serve static files from the frontend folder
app.use(express.static(path.join(__dirname, '../frontend')));

// MongoDB connection
const MONGO_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/student_depression';

//const MONGO_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/student_depression';

mongoose.connect('mongodb://localhost:27017/yourDB')
  .then(() => console.log('✅ MongoDB connected'))
  .catch((err) => console.error('❌ MongoDB connection error:', err));


// Routes
app.use('/', require('./src/routes/landing'));
app.use('/predictor', require('./src/routes/predictor'));
app.use('/journal', require('./src/routes/journal'));
app.use('/help', require('./src/routes/help'));
app.use('/content', require('./src/routes/content'));

// 404 Not Found handler
app.use((req, res) => {
  res.status(404).send('Not Found');
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('🔥 Internal Server Error:', err);
  res.status(500).json({ error: 'Internal Server Error' });
});

// Handle uncaught exceptions
process.on('uncaughtException', (err) => {
  console.error('🚨 Uncaught Exception:', err);
  process.exit(1);
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});

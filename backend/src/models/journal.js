const mongoose = require('mongoose');

const journalSchema = new mongoose.Schema({
  content: {
    type: String,
    required: true
  }
}, { timestamps: true });

module.exports = mongoose.model('Journal', journalSchema);

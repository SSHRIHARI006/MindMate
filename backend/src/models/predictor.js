const mongoose = require('mongoose');

const predictorSchema = new mongoose.Schema({
  age: { type: Number, required: true },
  degree: { type: String, required: true },
  course: { type: String, required: true },
  sleep: { type: Number, required: true },
  academicStress: { type: Number, required: true },
  studyHours: { type: Number, required: true },
  financialStress: { type: Number, required: true },
  suicidalThoughts: { type: Number, required: true },
  selfAssessment: { type: String, required: true }
});

module.exports = mongoose.model('Predictor', predictorSchema);

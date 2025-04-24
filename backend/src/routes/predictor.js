const express = require('express');
const router = express.Router();
const path = require('path');
const fetch = require('node-fetch');
const mongoose = require('mongoose');

const Predictor = require('/home/shrihari_006/programming/Student_Depression/backend/src/models/predictor.js');



const sleepMap = {
  "5-6 hours": 0,
  "7-8 hours": 1,
  "Less than 5 hours": 2,
  "More than 8 hours": 3,
  "Others": 4,
};

const suicidalMap = {
  "No": 0,
  "Yes": 1,
};

router.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../../../frontend/predictor.html'));
});

router.post('/submit', async (req, res) => {
  try {
    const data = req.body;

    const newEntry = new Predictor({
      age: data.age,
      degree: data.degree,
      course: data.course,
      sleep: sleepMap[data.sleep],
      academicStress: data.academic,
      studyHours: data.study,
      financialStress: data.stress,
      suicidalThoughts: suicidalMap[data.suicidal],
      selfAssessment: data.selfAssessment,
    });

    await newEntry.save();

    const predictionPayload = {
      sleep: data.sleep,
      academic: data.academic,
      diet: data.diet || "Moderate",
      study: data.study,
      stress: data.stress,
      suicidal: data.suicidal,
    };

    const response = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(predictionPayload),
    });

    if (!response.ok) {
      throw new Error(`FastAPI Error: ${response.statusText}`);
    }

    const result = await response.json();

    res.json({
      prediction: result.prediction,
      confidence: result.confidence,
      message:
        result.prediction === 'Yes'
          ? '⚠️ You might be at risk. Consider seeking support.'
          : '✅ You seem okay, but always take care of your mental health.',
    });
  } catch (err) {
    console.error('Error in /predictor/submit:', err.message);
    res.status(500).json({ error: 'Server error during prediction', detail: err.message });
  }
});

module.exports = router;
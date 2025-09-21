const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/", { 'dbName': 'dealershipsDB' });

const Reviews = require('./review');
const Dealerships = require('./dealership');

try {
  Reviews.deleteMany({}).then(() => {
    Reviews.insertMany(reviews_data['reviews']);
  });
  Dealerships.deleteMany({}).then(() => {
    Dealerships.insertMany(dealerships_data['dealerships']);
  });
} catch (error) {
  console.error('Error seeding database:', error);
}

// Home route
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// ✅ Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// ✅ Fetch reviews by dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// ✅ Fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const dealers = await Dealerships.find();
    res.json(dealers);
  } catch (error) {
    console.error("Error fetching dealers:", error);
    res.status(500).json({ error: 'Error fetching dealers' });
  }
});

// ✅ Fetch dealerships by state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = req.params.state;
    const dealers = await Dealerships.find({ state: state });
    if (dealers.length === 0) {
      return res.status(404).json({ message: "No dealers found in this state" });
    }
    res.json(dealers);
  } catch (error) {
    console.error("Error fetching dealers by state:", error);
    res.status(500).json({ error: 'Error fetching dealers by state' });
  }
});

// ✅ Fetch dealer by ID
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id); // dealer IDs are integers in JSON
    const dealer = await Dealerships.findOne({ id: dealerId });
    if (!dealer) {
      return res.status(404).json({ message: "Dealer not found" });
    }
    res.json(dealer);
  } catch (error) {
    console.error("Error fetching dealer by ID:", error);
    res.status(500).json({ error: 'Error fetching dealer by ID' });
  }
});

// ✅ Insert new review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  const data = JSON.parse(req.body);
  const documents = await Reviews.find().sort({ id: -1 });
  let new_id = documents[0]['id'] + 1;

  const review = new Reviews({
    "id": new_id,
    "name": data['name'],
    "dealership": data['dealership'],
    "review": data['review'],
    "purchase": data['purchase'],
    "purchase_date": data['purchase_date'],
    "car_make": data['car_make'],
    "car_model": data['car_model'],
    "car_year": data['car_year'],
  });

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// ✅ Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

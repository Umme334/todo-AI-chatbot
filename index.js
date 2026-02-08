// Todo AI Chatbot Application
const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static('public'));

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Basic API routes for todos
app.get('/api/todos', (req, res) => {
  // Return list of todos
  res.json([]);
});

app.post('/api/todos', (req, res) => {
  // Create a new todo
  const { task } = req.body;
  res.json({ id: Date.now(), task, completed: false });
});

app.listen(PORT, () => {
  console.log(`Todo AI Chatbot server running on port ${PORT}`);
});
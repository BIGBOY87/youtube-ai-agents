const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Healthy standard endpoints
app.get('/dashboard', (req, res) => {
  res.status(200).send('Dashboard Ready');
});

app.get('/api/upload/status', (req, res) => {
  res.status(200).json({ status: 'ready' });
});

/**
 * FIX TASK 4: Enhanced Error Logging for /api/drive/status 
 * Prevents silent 500 crashes that block Render's port verification
 */
app.get('/api/drive/status', async (req, res) => {
  try {
    // Simulated drive connection check - replace with your actual integration logic
    // e.g., await googleDrive.about.get(...)
    const driveConnected = true; 

    if (!driveConnected) {
      throw new Error("Drive service initialized but connection handshake failed.");
    }

    res.status(200).json({ status: 'connected', integration: 'active' });
  } catch (error) {
    // Full production stack tracing to pinpoint the 500 failure immediately
    console.error('--- CRITICAL ERROR: /api/drive/status ---');
    console.error('Message:', error.message);
    console.error('Stack:', error.stack);
    console.error('-----------------------------------------');
    
    res.status(500).json({ 
      error: 'Internal Server Error', 
      message: error.message,
      hint: 'Verify third-party drive API keys and environment credentials in Render dashboard'
    });
  }
});

// Serving static files if running monolithic deployment
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, '../frontend/dist')));
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/dist', 'index.html'));
  });
}

/**
 * FIX TASKS 1 & 2: Dynamic Port Bind & Absolute single server instantiation
 * Stripped any duplicate process.env setups or hardcoded localhost variations
 */
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
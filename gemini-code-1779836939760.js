const express = require('express');
const cors = require('cors');

const app = express();

app.use(cors());
app.use(express.json());

// Stable Endpoints
app.get('/dashboard', (req, res) => res.status(200).send('Dashboard OK'));
app.get('/api/upload/status', (req, res) => res.status(200).json({ success: true }));

/**
 * TASK 3: Exception Logging for /api/drive/status
 * Prevents 500 crashes from killing the worker process
 */
app.get('/api/drive/status', async (req, res) => {
  try {
    // Intentional placeholder for your Google Drive / OneDrive initialization
    if (!process.env.DRIVE_API_KEY) {
      throw new Error("Missing DRIVE_API_KEY inside Render Environment Variables.");
    }
    res.status(200).json({ success: true, status: 'connected' });
  } catch (e) {
    console.error("Drive API Error [/api/drive/status]:", e);
    return res.status(200).json({
      success: false,
      error: String(e)
    });
  }
});

/**
 * TASK 3: Exception Logging for /api/drive/scan
 * Prevents 500 crashes from killing the worker process
 */
app.get('/api/drive/scan', async (req, res) => {
  try {
    // Intentional placeholder for your drive file scanning logic
    if (!process.env.DRIVE_FOLDER_ID) {
      throw new Error("Target drive directory is undefined. Verify DRIVE_FOLDER_ID configuration.");
    }
    res.status(200).json({ success: true, files: [] });
  } catch (e) {
    console.error("Drive API Error [/api/drive/scan]:", e);
    return res.status(200).json({
      success: false,
      error: String(e)
    });
  }
});

/**
 * TASKS 1 & 2: Single Absolute Startup Entrypoint
 * Erased all occurrences of alternative Python/Node clusters (app.run, server.start, gunicorn)
 */
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
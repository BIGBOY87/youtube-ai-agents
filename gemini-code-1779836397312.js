// TASK 1 & 6: Cleaned API references. No hardcoded localhost or port 3000 variables.

export const getDashboardData = async () => {
  const response = await fetch('/dashboard');
  if (!response.ok) throw new Error('Failed to fetch dashboard context');
  return response.text();
};

export const getUploadStatus = async () => {
  const response = await fetch('/api/upload/status');
  if (!response.ok) throw new Error('Failed to fetch upload pipeline status');
  return response.json();
};

export const getDriveStatus = async () => {
  try {
    const response = await fetch('/api/drive/status');
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `Server responded with status ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Frontend API Exception [/api/drive/status]:', error.message);
    throw error;
  }
};
// Removed all 'http://localhost:3000' prefixes to utilize relative paths for Render compatibility

export const fetchHealthStatus = async () => {
  try {
    const response = await fetch('/api/health');
    if (!response.ok) throw new Error('Network response was not ok');
    return await response.json();
  } catch (error) {
    console.error('Error fetching health status:', error);
    throw error;
  }
};

export const fetchUsers = async () => {
  try {
    const response = await fetch('/api/users');
    if (!response.ok) throw new Error('Network response was not ok');
    return await response.json();
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};
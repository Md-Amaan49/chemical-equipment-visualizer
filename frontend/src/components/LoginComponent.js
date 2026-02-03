import React, { useState } from 'react';
import { login } from '../services/api';
import './LoginComponent.css';

const LoginComponent = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await login(username, password);
      onLogin(response.data.user);
    } catch (error) {
      setError(error.response?.data?.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h2>Chemical Equipment Visualizer</h2>
        <p>Please login to access the application</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={loading}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
            />
          </div>
          
          {error && <div className="error-message">{error}</div>}
          
          <button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        <div className="demo-credentials">
          <p><strong>Demo credentials:</strong></p>
          <p>Username: admin</p>
          <p>Password: admin123</p>
        </div>
      </div>
    </div>
  );
};

export default LoginComponent;
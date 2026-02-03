import React, { useState } from 'react';
import FileUploadComponent from './FileUploadComponent';
import DataVisualizationComponent from './DataVisualizationComponent';
import HistoryComponent from './HistoryComponent';
import { logout } from '../services/api';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState('upload');
  const [currentDataset, setCurrentDataset] = useState(null);

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      onLogout();
    }
  };

  const handleDatasetUploaded = (dataset) => {
    setCurrentDataset(dataset);
    setActiveTab('visualization');
  };

  const handleDatasetSelected = (dataset) => {
    setCurrentDataset(dataset);
    setActiveTab('visualization');
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Chemical Equipment Parameter Visualizer</h1>
        <div className="user-info">
          <span>Welcome, {user.username}</span>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </header>

      <nav className="dashboard-nav">
        <button
          className={activeTab === 'upload' ? 'active' : ''}
          onClick={() => setActiveTab('upload')}
        >
          Upload Data
        </button>
        <button
          className={activeTab === 'visualization' ? 'active' : ''}
          onClick={() => setActiveTab('visualization')}
          disabled={!currentDataset}
        >
          Visualization
        </button>
        <button
          className={activeTab === 'history' ? 'active' : ''}
          onClick={() => setActiveTab('history')}
        >
          History
        </button>
      </nav>

      <main className="dashboard-content">
        {activeTab === 'upload' && (
          <FileUploadComponent onDatasetUploaded={handleDatasetUploaded} />
        )}
        
        {activeTab === 'visualization' && currentDataset && (
          <DataVisualizationComponent dataset={currentDataset} />
        )}
        
        {activeTab === 'history' && (
          <HistoryComponent onDatasetSelected={handleDatasetSelected} />
        )}
      </main>
    </div>
  );
};

export default Dashboard;
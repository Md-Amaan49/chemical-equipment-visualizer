import React, { useState, useEffect } from 'react';
import { getHistory, deleteDataset } from '../services/api';
import './HistoryComponent.css';

const HistoryComponent = ({ onDatasetSelected }) => {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await getHistory();
      setDatasets(response.data.datasets);
    } catch (error) {
      setError('Failed to load history');
      console.error('History error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (datasetId, filename) => {
    if (!window.confirm(`Are you sure you want to delete "${filename}"?`)) {
      return;
    }

    try {
      await deleteDataset(datasetId);
      setDatasets(datasets.filter(dataset => dataset.id !== datasetId));
    } catch (error) {
      setError('Failed to delete dataset');
      console.error('Delete error:', error);
    }
  };

  const handleSelect = (dataset) => {
    onDatasetSelected(dataset);
  };

  if (loading) {
    return <div className="loading">Loading history...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (datasets.length === 0) {
    return (
      <div className="history-container">
        <h2>Dataset History</h2>
        <div className="empty-state">
          <p>No datasets uploaded yet.</p>
          <p>Upload your first CSV file to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="history-container">
      <h2>Dataset History</h2>
      <p>Your last {datasets.length} uploaded datasets</p>
      
      <div className="datasets-grid">
        {datasets.map((dataset) => (
          <div key={dataset.id} className="dataset-card">
            <div className="dataset-header">
              <h3>{dataset.filename}</h3>
              <div className="dataset-actions">
                <button
                  onClick={() => handleSelect(dataset)}
                  className="select-btn"
                  title="View this dataset"
                >
                  📊
                </button>
                <button
                  onClick={() => handleDelete(dataset.id, dataset.filename)}
                  className="delete-btn"
                  title="Delete this dataset"
                >
                  🗑️
                </button>
              </div>
            </div>
            
            <div className="dataset-info">
              <div className="info-item">
                <span className="label">Records:</span>
                <span className="value">{dataset.record_count}</span>
              </div>
              <div className="info-item">
                <span className="label">Uploaded:</span>
                <span className="value">
                  {new Date(dataset.upload_time).toLocaleDateString()}
                </span>
              </div>
            </div>
            
            <div className="dataset-summary">
              <h4>Summary Statistics</h4>
              <div className="summary-grid">
                <div className="summary-item">
                  <span className="summary-label">Avg Flowrate</span>
                  <span className="summary-value">
                    {dataset.summary.avg_flowrate.toFixed(2)}
                  </span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Avg Pressure</span>
                  <span className="summary-value">
                    {dataset.summary.avg_pressure.toFixed(2)}
                  </span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Avg Temperature</span>
                  <span className="summary-value">
                    {dataset.summary.avg_temperature.toFixed(2)}
                  </span>
                </div>
              </div>
              
              <div className="equipment-types">
                <h5>Equipment Types</h5>
                <div className="types-list">
                  {Object.entries(dataset.summary.type_distribution).map(([type, count]) => (
                    <span key={type} className="type-badge">
                      {type}: {count}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HistoryComponent;
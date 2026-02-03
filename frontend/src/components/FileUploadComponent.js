import React, { useState, useRef } from 'react';
import { uploadCSV } from '../services/api';
import './FileUploadComponent.css';

const FileUploadComponent = ({ onDatasetUploaded }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (selectedFile) => {
    setError('');
    setSuccess('');
    
    if (!selectedFile.name.endsWith('.csv')) {
      setError('Please select a CSV file');
      return;
    }
    
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }
    
    setFile(selectedFile);
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      handleFileSelect(selectedFile);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      handleFileSelect(droppedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const response = await uploadCSV(file);
      setSuccess(`File uploaded successfully! ${response.data.record_count} records processed.`);
      onDatasetUploaded({
        id: response.data.dataset_id,
        filename: response.data.filename,
        record_count: response.data.record_count,
        summary: response.data.summary
      });
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      setError(error.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="file-upload-container">
      <h2>Upload Equipment Data</h2>
      <p>Upload a CSV file containing chemical equipment data with columns: Equipment Name, Type, Flowrate, Pressure, Temperature</p>
      
      <div
        className={`drop-zone ${dragOver ? 'drag-over' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleBrowseClick}
      >
        <div className="drop-zone-content">
          <div className="upload-icon">📁</div>
          <p>Drag and drop your CSV file here, or click to browse</p>
          <p className="file-requirements">Max file size: 10MB | Format: CSV</p>
        </div>
      </div>

      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept=".csv"
        style={{ display: 'none' }}
      />

      {file && (
        <div className="file-info">
          <h3>Selected File:</h3>
          <p><strong>Name:</strong> {file.name}</p>
          <p><strong>Size:</strong> {(file.size / 1024).toFixed(2)} KB</p>
          <p><strong>Type:</strong> {file.type || 'text/csv'}</p>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="upload-actions">
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="upload-btn"
        >
          {uploading ? 'Uploading...' : 'Upload and Process'}
        </button>
        
        {file && (
          <button
            onClick={() => {
              setFile(null);
              setError('');
              setSuccess('');
              if (fileInputRef.current) {
                fileInputRef.current.value = '';
              }
            }}
            className="clear-btn"
          >
            Clear
          </button>
        )}
      </div>

      <div className="sample-data-info">
        <h3>Sample Data Format:</h3>
        <div className="sample-table">
          <table>
            <thead>
              <tr>
                <th>Equipment Name</th>
                <th>Type</th>
                <th>Flowrate</th>
                <th>Pressure</th>
                <th>Temperature</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Pump-001</td>
                <td>Pump</td>
                <td>45.2</td>
                <td>12.5</td>
                <td>298.15</td>
              </tr>
              <tr>
                <td>Valve-001</td>
                <td>Valve</td>
                <td>0.0</td>
                <td>15.2</td>
                <td>295.0</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default FileUploadComponent;
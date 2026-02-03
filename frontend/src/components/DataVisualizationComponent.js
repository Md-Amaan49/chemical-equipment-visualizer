import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import { getAnalytics } from '../services/api';
import './DataVisualizationComponent.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const DataVisualizationComponent = ({ dataset }) => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeChart, setActiveChart] = useState('averages');

  useEffect(() => {
    const loadAnalyticsData = async () => {
      if (dataset && dataset.id) {
        setLoading(true);
        setError('');
        
        try {
          const response = await getAnalytics(dataset.id);
          setAnalyticsData(response.data);
        } catch (error) {
          setError('Failed to load analytics data');
          console.error('Analytics error:', error);
        } finally {
          setLoading(false);
        }
      }
    };

    loadAnalyticsData();
  }, [dataset]);

  if (loading) {
    return <div className="loading">Loading analytics...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!analyticsData) {
    return <div className="error-message">No analytics data available</div>;
  }

  const { summary, equipment_records, metadata } = analyticsData;

  // Chart data for averages
  const averagesChartData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [
          summary.averages.flowrate,
          summary.averages.pressure,
          summary.averages.temperature,
        ],
        backgroundColor: [
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(255, 205, 86, 0.6)',
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(255, 205, 86, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  // Chart data for equipment type distribution
  const typeDistributionData = {
    labels: Object.keys(summary.type_distribution),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(summary.type_distribution),
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 205, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 205, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: activeChart === 'averages' ? 'Average Parameter Values' : 'Equipment Type Distribution',
      },
    },
  };

  return (
    <div className="data-visualization-container">
      <div className="dataset-info">
        <h2>Dataset Analysis: {metadata.filename}</h2>
        <div className="metadata">
          <span>Records: {metadata.record_count}</span>
          <span>Uploaded: {new Date(metadata.upload_time).toLocaleString()}</span>
        </div>
      </div>

      <div className="summary-cards">
        <div className="summary-card">
          <h3>Total Equipment</h3>
          <div className="summary-value">{summary.total_count}</div>
        </div>
        <div className="summary-card">
          <h3>Avg Flowrate</h3>
          <div className="summary-value">{summary.averages.flowrate.toFixed(2)}</div>
        </div>
        <div className="summary-card">
          <h3>Avg Pressure</h3>
          <div className="summary-value">{summary.averages.pressure.toFixed(2)}</div>
        </div>
        <div className="summary-card">
          <h3>Avg Temperature</h3>
          <div className="summary-value">{summary.averages.temperature.toFixed(2)}</div>
        </div>
      </div>

      <div className="chart-controls">
        <button
          className={activeChart === 'averages' ? 'active' : ''}
          onClick={() => setActiveChart('averages')}
        >
          Parameter Averages
        </button>
        <button
          className={activeChart === 'distribution' ? 'active' : ''}
          onClick={() => setActiveChart('distribution')}
        >
          Equipment Distribution
        </button>
      </div>

      <div className="chart-container">
        {activeChart === 'averages' ? (
          <Bar data={averagesChartData} options={chartOptions} />
        ) : (
          <Pie data={typeDistributionData} options={chartOptions} />
        )}
      </div>

      <div className="equipment-table">
        <h3>Equipment Records</h3>
        <div className="table-container">
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
              {equipment_records.map((record, index) => (
                <tr key={index}>
                  <td>{record.equipment_name}</td>
                  <td>{record.equipment_type}</td>
                  <td>{record.flowrate.toFixed(2)}</td>
                  <td>{record.pressure.toFixed(2)}</td>
                  <td>{record.temperature.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DataVisualizationComponent;
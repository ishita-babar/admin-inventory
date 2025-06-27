import React, { useState } from 'react';
import Layout from '../components/Layout';
import ForecastTable from '../components/ForecastTable';
import { forecastApi, ForecastResult } from '../lib/api';
import { Brain, Loader, RefreshCw } from 'lucide-react';

export default function Forecast() {
  const [forecasts, setForecasts] = useState<ForecastResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [lastGenerated, setLastGenerated] = useState<Date | null>(null);

  const generateForecast = async () => {
    setLoading(true);
    try {
      const data = await forecastApi.generate();
      setForecasts(data);
      setLastGenerated(new Date());
    } catch (error) {
      console.error('Failed to generate forecast:', error);
      alert('Failed to generate forecast. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getActionSummary = () => {
    const summary = forecasts.reduce((acc, forecast) => {
      acc[forecast.action] = (acc[forecast.action] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return summary;
  };

  const actionSummary = getActionSummary();

  return (
    <Layout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-default">ML Forecast</h1>
          <p className="text-default/70 mt-2">AI-powered demand prediction and recommendations</p>
        </div>

        {/* Generate Forecast Button */}
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-primary">Generate Forecast</h2>
              <p className="text-primary/70 mt-1">
                Analyze inventory, sales, and user intent data to predict demand
              </p>
              {lastGenerated && (
                <p className="text-sm text-primary/50 mt-1">
                  Last generated: {lastGenerated.toLocaleString()}
                </p>
              )}
            </div>
            <button
              onClick={generateForecast}
              disabled={loading}
              className="btn-primary flex items-center space-x-2"
            >
              {loading ? (
                <Loader className="w-5 h-5 animate-spin" />
              ) : (
                <Brain className="w-5 h-5" />
              )}
              <span>{loading ? 'Generating...' : 'Generate Forecast'}</span>
            </button>
          </div>
        </div>

        {/* Action Summary */}
        {forecasts.length > 0 && (
          <div className="card">
            <h3 className="text-lg font-semibold text-primary mb-4">Action Summary</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(actionSummary).map(([action, count]) => (
                <div key={action} className="text-center p-4 bg-neutral/30 rounded-lg">
                  <p className="text-2xl font-bold text-primary">{count}</p>
                  <p className="text-sm text-primary/70">{action}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Forecast Results */}
        {forecasts.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-semibold text-primary">Forecast Results</h2>
              <button
                onClick={generateForecast}
                disabled={loading}
                className="btn-secondary flex items-center space-x-2"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                <span>Refresh</span>
              </button>
            </div>
            <ForecastTable forecasts={forecasts} />
          </div>
        )}

        {/* Empty State */}
        {forecasts.length === 0 && !loading && (
          <div className="card text-center py-12">
            <Brain className="w-16 h-16 text-primary/30 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-primary mb-2">No Forecast Data</h3>
            <p className="text-primary/70 mb-6">
              Click "Generate Forecast" to analyze your inventory and get AI-powered recommendations.
            </p>
            <button
              onClick={generateForecast}
              className="btn-primary"
            >
              Generate Your First Forecast
            </button>
          </div>
        )}
      </div>
    </Layout>
  );
} 
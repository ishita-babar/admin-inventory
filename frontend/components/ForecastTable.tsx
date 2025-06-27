import React from 'react';
import { ForecastResult } from '../lib/api';
import { getActionColor, getConfidenceColor } from '../lib/utils';

interface ForecastTableProps {
  forecasts: ForecastResult[];
}

export default function ForecastTable({ forecasts }: ForecastTableProps) {
  return (
    <div className="card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="table-header">
              <th className="px-6 py-3 text-left">Product</th>
              <th className="px-6 py-3 text-left">Category</th>
              <th className="px-6 py-3 text-left">Current Stock</th>
              <th className="px-6 py-3 text-left">Predicted Demand</th>
              <th className="px-6 py-3 text-left">Action</th>
              <th className="px-6 py-3 text-left">Confidence</th>
              <th className="px-6 py-3 text-left">Reason</th>
            </tr>
          </thead>
          <tbody>
            {forecasts.map((forecast, index) => (
              <tr key={index} className="table-row border-b border-neutral">
                <td className="px-6 py-4">
                  <div>
                    <p className="font-medium text-primary">{forecast.product_name}</p>
                    <p className="text-sm text-primary/70">{forecast.sku_id}</p>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm text-primary">{forecast.category}</span>
                </td>
                <td className="px-6 py-4">
                  <span className="font-medium">{forecast.current_stock}</span>
                </td>
                <td className="px-6 py-4">
                  <span className="font-medium">{forecast.predicted_demand}</span>
                </td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getActionColor(forecast.action)}`}>
                    {forecast.action}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getConfidenceColor(forecast.confidence)}`}>
                    {forecast.confidence}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm text-primary/70 max-w-xs truncate block" title={forecast.reason}>
                    {forecast.reason}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
} 
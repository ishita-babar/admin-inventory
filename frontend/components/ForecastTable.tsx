import React, { useEffect, useState } from 'react';
import { ForecastResult } from '../lib/api';
import { getActionColor } from '../lib/utils';

interface ForecastTableProps {
  forecasts: ForecastResult[];
}

const PAGE_SIZE = 10;
const PAGE_KEY = 'forecastTablePage';

function getForecastsHash(forecasts: ForecastResult[]): string {
  if (!forecasts.length) return '0';
  return `${forecasts.length}-${forecasts[0].sku_id}-${forecasts[forecasts.length - 1].sku_id}`;
}

export default function ForecastTable({ forecasts }: ForecastTableProps) {
  const [page, setPage] = useState(0);
  const [dataHash, setDataHash] = useState('');

  useEffect(() => {
    const hash = getForecastsHash(forecasts);
    setDataHash(hash);
    const saved = localStorage.getItem(PAGE_KEY);
    if (saved && hash === localStorage.getItem(PAGE_KEY + '_hash')) {
      setPage(Number(saved));
    } else {
      setPage(0);
      localStorage.setItem(PAGE_KEY, '0');
      localStorage.setItem(PAGE_KEY + '_hash', hash);
    }
  }, [forecasts]);

  useEffect(() => {
    localStorage.setItem(PAGE_KEY, String(page));
    localStorage.setItem(PAGE_KEY + '_hash', dataHash);
  }, [page, dataHash]);

  const totalPages = Math.ceil(forecasts.length / PAGE_SIZE);
  const start = page * PAGE_SIZE;
  const end = start + PAGE_SIZE;
  const pageForecasts = forecasts.slice(start, end);

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
              <th className="px-6 py-3 text-left">Reason</th>
            </tr>
          </thead>
          <tbody>
            {pageForecasts.map((forecast, index) => (
              <tr key={start + index} className="table-row border-b border-neutral">
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
                  <span className="font-medium text-primary">{forecast.current_stock}</span>
                </td>
                <td className="px-6 py-4">
                  <span className="font-medium text-primary">{forecast.predicted_demand}</span>
                </td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 rounded-full text-xs font-medium text-primary">
                    {forecast.action}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm text-primary/70 max-w-xs whitespace-pre-line break-words block">
                    {forecast.reason}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Pagination Controls */}
      <div className="flex justify-between items-center p-4">
        <button
          className="btn-secondary px-4 py-2 rounded disabled:opacity-50"
          onClick={() => setPage((p) => Math.max(0, p - 1))}
          disabled={page === 0}
        >
          Previous
        </button>
        <span className="text-sm text-primary">
          Page {page + 1} of {totalPages}
        </span>
        <button
          className="btn-secondary px-4 py-2 rounded disabled:opacity-50"
          onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
          disabled={page >= totalPages - 1}
        >
          Next
        </button>
      </div>
    </div>
  );
} 
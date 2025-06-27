import React from 'react';
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
// import { Product } from '../lib/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface CategoryDatum {
  category: string;
  revenue: number;
  units: number;
}

interface TrendChartsProps {
  categoryData?: CategoryDatum[];
  products?: any[]; // for backward compatibility
}

export default function TrendCharts({ categoryData, products }: TrendChartsProps) {
  let categories: string[] = [];
  let unitsData: number[] = [];
  let revenueData: number[] = [];

  if (categoryData) {
    categories = categoryData.map(d => d.category);
    unitsData = categoryData.map(d => d.units);
    revenueData = categoryData.map(d => d.revenue);
  } else if (products) {
    // fallback for old usage
    const categoryMap: Record<string, { units: number; revenue: number }> = {};
    products.forEach((p) => {
      const cat = p.category?.name || p.category || 'Unknown';
      if (!categoryMap[cat]) categoryMap[cat] = { units: 0, revenue: 0 };
      categoryMap[cat].units += p.inventoryCount || Number(p.units_in_stock) || 0;
      categoryMap[cat].revenue += (p.price || 0) * (p.inventoryCount || Number(p.units_in_stock) || 0);
    });
    categories = Object.keys(categoryMap);
    unitsData = categories.map(cat => categoryMap[cat].units);
    revenueData = categories.map(cat => categoryMap[cat].revenue);
  }

  const barChartData = {
    labels: categories,
    datasets: [
      {
        label: 'Units by Category',
        data: unitsData,
        backgroundColor: '#2563eb',
        borderColor: '#1e293b',
        borderWidth: 1,
      },
    ],
  };

  const pieChartData = {
    labels: categories,
    datasets: [
      {
        data: revenueData,
        backgroundColor: [
          '#1e293b',
          '#2563eb',
          '#3b82f6',
          '#60a5fa',
          '#0f172a',
        ],
        borderWidth: 2,
        borderColor: '#ffffff',
      },
    ],
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Units by Category',
        color: '#1e293b',
        font: {
          size: 16,
          weight: 700,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: '#e5e7eb',
        },
        ticks: {
          color: '#1e293b',
        },
      },
      x: {
        grid: {
          color: '#e5e7eb',
        },
        ticks: {
          color: '#1e293b',
        },
      },
    },
  };

  const pieOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Revenue by Category',
        color: '#1e293b',
        font: {
          size: 16,
          weight: 700,
        },
      },
    },
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="card">
        <Bar data={barChartData} options={barOptions} />
      </div>
      <div className="card">
        <Pie data={pieChartData} options={pieOptions} />
      </div>
    </div>
  );
} 
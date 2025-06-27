import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricTileProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  change?: string;
  changeType?: 'positive' | 'negative' | 'neutral';
}

export default function MetricTile({ title, value, icon: Icon, change, changeType }: MetricTileProps) {
  return (
    <div className="metric-card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-default">{title}</p>
          <p className="text-2xl font-bold text-default mt-1">{value}</p>
          {change && (
            <p className={`text-sm mt-1 ${
              changeType === 'positive' ? 'text-green-600' : 
              changeType === 'negative' ? 'text-red-600' : 
              'text-default'
            }`}>
              {change}
            </p>
          )}
        </div>
        <div className="p-3 bg-secondary/10 rounded-lg">
          <Icon className="w-6 h-6 text-blue-400" />
        </div>
      </div>
    </div>
  );
} 
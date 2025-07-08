import React, { useEffect, useState, useCallback } from 'react';
import Layout from '../components/Layout';
import MetricTile from '../components/MetricTile';
import TrendCharts from '../components/TrendCharts';
import ProductTable from '../components/ProductTable';
import { productApi, Product, ProductStats } from '../lib/api';
import { 
  Package, 
  TrendingUp,
  AlertTriangle,
  CheckCircle
} from 'lucide-react';

const MemoProductTable = React.memo(ProductTable);
const MemoTrendCharts = React.memo(TrendCharts);

export default function Dashboard() {
  const [products, setProducts] = useState<Product[]>([]);
  const [stats, setStats] = useState<ProductStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshFlag, setRefreshFlag] = useState(0);

  // Helper to compare arrays shallowly
  const shallowEqual = (a: any[], b: any[]) =>
    a.length === b.length && a.every((v, i) => v === b[i]);

  const fetchAndCacheData = useCallback(async () => {
    setLoading(true);
      try {
        const [productsData, statsData] = await Promise.all([
          productApi.getAll(),
          productApi.getStats()
        ]);
      // Only update if changed
      const cachedProducts = localStorage.getItem('dashboard_products');
      const cachedStats = localStorage.getItem('dashboard_stats');
      if (
        !cachedProducts ||
        !cachedStats ||
        JSON.stringify(productsData) !== cachedProducts ||
        JSON.stringify(statsData) !== cachedStats
      ) {
        setProducts(productsData);
        setStats(statsData);
        localStorage.setItem('dashboard_products', JSON.stringify(productsData));
        localStorage.setItem('dashboard_stats', JSON.stringify(statsData));
      }
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
  }, []);

  useEffect(() => {
    // Try to load from cache first
    const cachedProducts = localStorage.getItem('dashboard_products');
    const cachedStats = localStorage.getItem('dashboard_stats');
    if (cachedProducts && cachedStats) {
      setProducts(JSON.parse(cachedProducts));
      setStats(JSON.parse(cachedStats));
      setLoading(false);
    } else {
      fetchAndCacheData();
    }
  }, [fetchAndCacheData, refreshFlag]);

  const handleRefresh = () => {
    setLoading(true);
    setRefreshFlag(f => f + 1);
    setTimeout(fetchAndCacheData, 0);
  };

  const handleInventoryUpdate = async (productId: number, newCount: number) => {
    try {
      await productApi.updateInventory(productId, { inventoryCount: newCount });
      // Refresh data
      handleRefresh();
    } catch (error) {
      console.error('Failed to update inventory:', error);
      throw error;
    }
  };

  // Get top selling products (mock data for now)
  const topSellingProducts = products.slice(0, 5);

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="text-default">Loading dashboard...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-neutral">Dashboard</h1>
          <p className="text-neutral/70 mt-2">Monitor your inventory and sales performance</p>
          </div>
          <button
            className="ml-auto px-4 py-2 bg-secondary text-white rounded-lg hover:bg-secondary-dark"
            onClick={handleRefresh}
            disabled={loading}
          >
            Refresh
          </button>
        </div>

        {/* Metric Tiles */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 text-default">
          <MetricTile
            title="Total Products"
            value={stats?.totalProducts || 0}
            icon={Package}
          />
          <MetricTile
            title="Total Inventory"
            value={stats?.totalInventory || 0}
            icon={TrendingUp}
          />
          <MetricTile
            title="Low Stock Items"
            value={stats?.lowStockCount || 0}
            icon={AlertTriangle}
            changeType="negative"
          />
          <MetricTile
            title="Overstock Items"
            value={stats?.overstockCount || 0}
            icon={CheckCircle}
            changeType="neutral"
          />
        </div>

        {/* Sales Analytics */}
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold text-default">Sales Analytics</h2>
          <MemoTrendCharts products={products} />
        </div>

        {/* Top Selling Products */}
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold text-default">Top Selling Products</h2>
          <MemoProductTable 
            products={topSellingProducts} 
            onInventoryUpdate={handleInventoryUpdate}
          />
        </div>
      </div>
    </Layout>
  );
} 
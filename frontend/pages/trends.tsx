import React, { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import ProductTable from '../components/ProductTable';
import { productApi, Product } from '../lib/api';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function Trends() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const data = await productApi.getAll();
        setProducts(data);
      } catch (error) {
        console.error('Failed to fetch products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const handleInventoryUpdate = async (productId: number, newCount: number) => {
    try {
      await productApi.updateInventory(productId, { inventoryCount: newCount });
      // Refresh products
      const data = await productApi.getAll();
      setProducts(data);
    } catch (error) {
      console.error('Failed to update inventory:', error);
      throw error;
    }
  };

  // Calculate performance metrics (mock data for now)
  const topProducts = products.slice(0, 3);
  const bottomProducts = products.slice(-3).reverse();

  // Group by category for category performance
  const categoryPerformance = products.reduce((acc, product) => {
    const categoryName = product.category?.name || 'Unknown';
    if (!acc[categoryName]) {
      acc[categoryName] = {
        name: categoryName,
        productCount: 0,
        totalRevenue: 0,
        avgRating: 0,
      };
    }
    acc[categoryName].productCount += 1;
    acc[categoryName].totalRevenue += product.price * product.inventoryCount;
    return acc;
  }, {} as Record<string, any>);

  const categoryArray = Object.values(categoryPerformance);
  const topCategories = categoryArray.slice(0, 3);
  const bottomCategories = categoryArray.slice(-3).reverse();

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="text-primary">Loading trends...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-8">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-default">Monthly Trends</h1>
          <p className="text-default/70 mt-2">Top and bottom performing products and categories</p>
        </div>

        {/* Top Products */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-6 h-6 text-green-600" />
            <h2 className="text-2xl font-semibold text-default">Top 3 Products</h2>
          </div>
          <ProductTable 
            products={topProducts} 
            onInventoryUpdate={handleInventoryUpdate}
          />
        </div>

        {/* Bottom Products */}
        <div className="space-y-4">
          <div className="flex items-center space-x-2">
            <TrendingDown className="w-6 h-6 text-red-600" />
            <h2 className="text-2xl font-semibold text-default">Bottom 3 Products</h2>
          </div>
          <ProductTable 
            products={bottomProducts} 
            onInventoryUpdate={handleInventoryUpdate}
          />
        </div>

        {/* Category Performance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Top Categories */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-5 h-5 text-green-600" />
              <h3 className="text-xl font-semibold text-default">Top 3 Categories</h3>
            </div>
            <div className="card">
              <div className="space-y-4">
                {topCategories.map((category, index) => (
                  <div key={category.name} className="flex items-center justify-between p-4 bg-neutral/30 rounded-lg">
                    <div>
                      <p className="font-medium text-primary">{category.name}</p>
                      <p className="text-sm text-primary/70">{category.productCount} products</p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium text-primary">${category.totalRevenue.toFixed(2)}</p>
                      <p className="text-sm text-primary/70">Revenue</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Bottom Categories */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <TrendingDown className="w-5 h-5 text-red-600" />
              <h3 className="text-xl font-semibold text-default">Bottom 3 Categories</h3>
            </div>
            <div className="card">
              <div className="space-y-4">
                {bottomCategories.map((category, index) => (
                  <div key={category.name} className="flex items-center justify-between p-4 bg-neutral/30 rounded-lg">
                    <div>
                      <p className="font-medium text-primary">{category.name}</p>
                      <p className="text-sm text-primary/70">{category.productCount} products</p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium text-primary">${category.totalRevenue.toFixed(2)}</p>
                      <p className="text-sm text-primary/70">Revenue</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
} 
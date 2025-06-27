import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../components/Layout';
import ProductTable from '../../components/ProductTable';
import { productApi, Product } from '../../lib/api';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function CategoryPage() {
  const router = useRouter();
  const { id } = router.query;
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [categoryName, setCategoryName] = useState('');

  useEffect(() => {
    if (id) {
      const fetchCategoryProducts = async () => {
        try {
          const data = await productApi.getByCategory(Number(id));
          setProducts(data);
          if (data.length > 0) {
            setCategoryName(data[0].category?.name || 'Unknown Category');
          }
        } catch (error) {
          console.error('Failed to fetch category products:', error);
        } finally {
          setLoading(false);
        }
      };

      fetchCategoryProducts();
    }
  }, [id]);

  const handleInventoryUpdate = async (productId: number, newCount: number) => {
    try {
      await productApi.updateInventory(productId, { inventoryCount: newCount });
      // Refresh products
      const data = await productApi.getByCategory(Number(id));
      setProducts(data);
    } catch (error) {
      console.error('Failed to update inventory:', error);
      throw error;
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="text-primary">Loading category...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center space-x-4">
          <Link href="/" className="text-secondary hover:text-secondary-dark">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-primary">{categoryName}</h1>
            <p className="text-primary/70 mt-2">
              {products.length} products in this category
            </p>
          </div>
        </div>

        {/* Products Table */}
        <ProductTable 
          products={products} 
          onInventoryUpdate={handleInventoryUpdate}
          showCategory={false}
        />
      </div>
    </Layout>
  );
} 
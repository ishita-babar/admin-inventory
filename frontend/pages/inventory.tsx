import React, { useEffect, useState, useRef } from 'react';
import Layout from '../components/Layout';
import ProductTable from '../components/ProductTable';
import { productApi, Product } from '../lib/api';
import { Search, Filter } from 'lucide-react';

interface PaginatedProducts {
  content: Product[];
  totalPages: number;
  totalElements: number;
  number: number;
  size: number;
}

const PAGE_SIZE = 10;

export default function Inventory() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [filterMenuOpen, setFilterMenuOpen] = useState(false);
  const [page, setPage] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [totalElements, setTotalElements] = useState(0);
  const filterRef = useRef<HTMLDivElement>(null);

  // Fetch paginated products
  useEffect(() => {
    let cancelled = false;
    async function fetchPage() {
      setLoading(true);
      try {
        const data = await productApi.getPaginated(page, PAGE_SIZE) as PaginatedProducts;
        if (!cancelled) {
          setProducts(data.content);
          setTotalPages(data.totalPages);
          setTotalElements(data.totalElements);
        }
      } catch (error) {
        if (!cancelled) {
          setProducts([]);
          setTotalPages(1);
          setTotalElements(0);
        }
        console.error('Failed to fetch products:', error);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    fetchPage();
    return () => { cancelled = true; };
  }, [page]);

  // Filtering (client-side for current page only)
  const filteredProducts = products.filter(product => {
    const matchesSearch =
      product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.category?.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus =
      statusFilter === 'all' ||
      product.inventoryStatus.toLowerCase() === statusFilter.toLowerCase();
    return matchesSearch && matchesStatus;
  });

  // Close filter menu on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (filterRef.current && !filterRef.current.contains(event.target as Node)) {
        setFilterMenuOpen(false);
      }
    }
    if (filterMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [filterMenuOpen]);

  const handleInventoryUpdate = async (productId: number, newCount: number) => {
    try {
      await productApi.updateInventory(productId, { inventoryCount: newCount });
      // Refresh current page
      setLoading(true);
      const data = await productApi.getPaginated(page, PAGE_SIZE) as PaginatedProducts;
      setProducts(data.content);
      setTotalPages(data.totalPages);
      setTotalElements(data.totalElements);
      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.error('Failed to update inventory:', error);
      throw error;
    }
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-default">Inventory Management</h1>
          <p className="text-default/70 mt-2">Manage your product inventory and stock levels</p>
        </div>

        {/* Filters */}
        <div className="card">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search */}
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-primary/50 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search products, SKU, or category..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-black rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary focus:border-black"
                />
              </div>
            </div>

            {/* Status Filter */}
            <div className="flex items-center relative" ref={filterRef}>
              <button
                type="button"
                className="p-2 rounded-lg hover:bg-secondary/10 focus:outline-none"
                onClick={() => setFilterMenuOpen((open) => !open)}
                aria-label="Filter"
              >
                <Filter className="w-5 h-5 text-primary/50" />
              </button>
              {filterMenuOpen && (
                <div className="absolute right-0 mt-2 w-40 bg-white border border-neutral rounded-lg shadow-lg z-10">
                  <button
                    className={`block w-full text-left px-4 py-2 hover:bg-secondary/10 ${statusFilter === 'all' ? 'font-bold text-secondary' : 'text-primary'}`}
                    onClick={() => { setStatusFilter('all'); setFilterMenuOpen(false); }}
                  >All Status</button>
                  <button
                    className={`block w-full text-left px-4 py-2 hover:bg-secondary/10 ${statusFilter === 'in stock' ? 'font-bold text-secondary' : 'text-primary'}`}
                    onClick={() => { setStatusFilter('in stock'); setFilterMenuOpen(false); }}
                  >In Stock</button>
                  <button
                    className={`block w-full text-left px-4 py-2 hover:bg-secondary/10 ${statusFilter === 'low stock' ? 'font-bold text-secondary' : 'text-primary'}`}
                    onClick={() => { setStatusFilter('low stock'); setFilterMenuOpen(false); }}
                  >Low Stock</button>
                  <button
                    className={`block w-full text-left px-4 py-2 hover:bg-secondary/10 ${statusFilter === 'overstock' ? 'font-bold text-secondary' : 'text-primary'}`}
                    onClick={() => { setStatusFilter('overstock'); setFilterMenuOpen(false); }}
                  >Overstock</button>
                </div>
              )}
            </div>
          </div>

          {/* Results count */}
          <div className="mt-4 text-sm text-primary/70">
            Showing {filteredProducts.length} of {totalElements} products (page {page + 1} of {totalPages})
          </div>
        </div>

        {/* Products Table */}
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-primary">Loading inventory...</div>
          </div>
        ) : (
          <ProductTable 
            products={filteredProducts} 
            onInventoryUpdate={handleInventoryUpdate}
          />
        )}

        {/* Pagination Controls */}
        <div className="flex justify-center items-center gap-2 mt-4">
          <button
            className="px-3 py-1 rounded bg-secondary text-white disabled:opacity-50"
            onClick={() => setPage(p => Math.max(0, p - 1))}
            disabled={page === 0 || loading}
          >
            Previous
          </button>
          <span className="text-default">Page {page + 1} of {totalPages}</span>
          <button
            className="px-3 py-1 rounded bg-secondary text-white disabled:opacity-50"
            onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))}
            disabled={page >= totalPages - 1 || loading}
          >
            Next
          </button>
        </div>
      </div>
    </Layout>
  );
} 
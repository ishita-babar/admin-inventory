import React, { useState } from 'react';
import { Product } from '../lib/api';
import { formatCurrency, getStatusColor } from '../lib/utils';
import { Edit, Save, X } from 'lucide-react';

interface ProductTableProps {
  products: Product[];
  onInventoryUpdate: (productId: number, newCount: number) => Promise<void>;
  showCategory?: boolean;
}

export default function ProductTable({ products, onInventoryUpdate, showCategory = true }: ProductTableProps) {
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editValue, setEditValue] = useState<number>(0);
  const [loading, setLoading] = useState<number | null>(null);

  const handleEdit = (product: Product) => {
    setEditingId(product.id);
    setEditValue(product.inventoryCount);
  };

  const handleSave = async (productId: number) => {
    setLoading(productId);
    try {
      await onInventoryUpdate(productId, editValue);
      setEditingId(null);
    } catch (error) {
      console.error('Failed to update inventory:', error);
    } finally {
      setLoading(null);
    }
  };

  const handleCancel = () => {
    setEditingId(null);
  };

  return (
    <div className="card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="table-header">
              <th className="px-6 py-3 text-left">Product</th>
              {showCategory && <th className="px-6 py-3 text-left">Category</th>}
              <th className="px-6 py-3 text-left">Price</th>
              <th className="px-6 py-3 text-left">Status</th>
              <th className="px-6 py-3 text-left">Inventory</th>
              <th className="px-6 py-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id} className="table-row border-b border-neutral">
                <td className="px-6 py-4">
                  <div>
                    <p className="font-medium text-primary">{product.name}</p>
                    <p className="text-sm text-primary/70">{product.sku}</p>
                  </div>
                </td>
                {showCategory && (
                  <td className="px-6 py-4">
                    <span className="text-sm text-primary">{product.category?.name}</span>
                  </td>
                )}
                <td className="px-6 py-4">
                  <span className="font-medium text-black">{formatCurrency(product.price)}</span>
                </td>
                <td className="px-6 py-4">
                  {(() => {
                    let status = product.inventoryStatus?.toLowerCase();
                    let label = 'In Stock';
                    let color = 'bg-blue-900 text-white';
                    let dot = 'bg-blue-400';
                    if (status === 'low stock') {
                      label = 'Low Stock';
                      color = 'bg-yellow-600 text-white';
                      dot = 'bg-yellow-300';
                    } else if (status === 'overstock') {
                      label = 'Overstock';
                      color = 'bg-green-700 text-white';
                      dot = 'bg-green-300';
                    }
                    return (
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${color}`}
                        style={{ minWidth: 90, justifyContent: 'center' }}>
                        <span className={`w-2 h-2 rounded-full mr-2 ${dot}`}></span>
                        {label}
                      </span>
                    );
                  })()}
                </td>
                <td className="px-6 py-4">
                  {editingId === product.id ? (
                    <input
                      type="number"
                      value={editValue}
                      onChange={(e) => setEditValue(parseInt(e.target.value) || 0)}
                      className="w-20 px-2 py-1 border border-neutral rounded text-sm text-black"
                      min="0"
                    />
                  ) : (
                    <span className="font-medium text-black">{product.inventoryCount}</span>
                  )}
                </td>
                <td className="px-6 py-4">
                  {editingId === product.id ? (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleSave(product.id)}
                        disabled={loading === product.id}
                        className="p-1 text-green-600 hover:bg-green-100 rounded"
                      >
                        <Save className="w-4 h-4" />
                      </button>
                      <button
                        onClick={handleCancel}
                        className="p-1 text-red-600 hover:bg-red-100 rounded"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  ) : (
                    <button
                      onClick={() => handleEdit(product)}
                      className="p-1 text-secondary hover:bg-secondary/10 rounded"
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
} 
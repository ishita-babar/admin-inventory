import axios from 'axios';

const API_BASE_URL = 'http://localhost:8080/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Product {
  id: number;
  sku: string;
  name: string;
  description: string;
  category: Category;
  price: number;
  inventoryCount: number;
  minStockLevel: number;
  maxStockLevel: number;
  inventoryStatus: string;
}

export interface Category {
  id: number;
  name: string;
  description: string;
}

export interface InventoryUpdate {
  inventoryCount: number;
}

export interface ForecastResult {
  sku_id: string;
  product_name: string;
  category: string;
  predicted_demand: number;
  current_stock: number;
  action: string;
  confidence: string;
  reason: string;
  metrics: {
    sales_velocity: number;
    return_rate: number;
    avg_rating: number;
    cart_activity: number;
    wishlist_activity: number;
  };
}

export interface ProductStats {
  totalProducts: number;
  totalInventory: number;
  lowStockCount: number;
  overstockCount: number;
}

// Product API calls
export const productApi = {
  getAll: () => api.get<Product[]>('/products').then(res => res.data),
  getById: (id: number) => api.get<Product>(`/products/${id}`).then(res => res.data),
  getByCategory: (categoryId: number) => api.get<Product[]>(`/products/category/${categoryId}`).then(res => res.data),
  updateInventory: (id: number, update: InventoryUpdate) => api.patch<Product>(`/products/${id}`, update).then(res => res.data),
  getLowStock: () => api.get<Product[]>('/products/low-stock').then(res => res.data),
  getOverstock: () => api.get<Product[]>('/products/overstock').then(res => res.data),
  getStats: () => api.get<ProductStats>('/products/stats').then(res => res.data),
  getPaginated: (page: number, size: number) =>
    api.get(`/products/page?page=${page}&size=${size}`).then(res => res.data),
};

// Forecast API calls
export const forecastApi = {
  generate: () => api.post<ForecastResult[]>('/forecast').then(res => res.data),
  getStatus: () => api.get('/forecast/status').then(res => res.data),
};

export default api; 
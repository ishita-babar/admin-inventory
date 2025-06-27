import Papa from 'papaparse';

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

export function getStatusColor(status: string): string {
  switch (status.toLowerCase()) {
    case 'low stock':
      return 'text-blue-600 bg-blue-100';
    case 'overstock':
      return 'text-blue-400 bg-blue-50';
    case 'in stock':
      return 'text-black bg-white';
    default:
      return 'text-gray-600 bg-gray-100';
  }
}

export function getActionColor(action: string): string {
  switch (action) {
    case 'RESTOCK':
      return 'text-blue-600 bg-blue-100';
    case 'DISCOUNT':
      return 'text-blue-400 bg-blue-50';
    case 'DEPRECATE':
      return 'text-black bg-white';
    case 'NO ACTION':
      return 'text-white bg-blue-600';
    default:
      return 'text-gray-600 bg-gray-100';
  }
}

export function getConfidenceColor(confidence: string): string {
  switch (confidence) {
    case 'HIGH':
      return 'text-blue-600 bg-blue-100';
    case 'MEDIUM':
      return 'text-blue-400 bg-blue-50';
    case 'LOW':
      return 'text-black bg-white';
    default:
      return 'text-gray-600 bg-gray-100';
  }
}

// CSV parsing utility (requires papaparse)
// If not installed, run: npm install papaparse
export async function fetchProductsCSV(): Promise<any[]> {
  const response = await fetch('/products.csv');
  const csvText = await response.text();
  return new Promise((resolve, reject) => {
    Papa.parse(csvText, {
      header: true,
      skipEmptyLines: true,
      complete: (results: Papa.ParseResult<any>) => resolve(results.data),
      error: (err: Error) => reject(err),
    });
  });
} 
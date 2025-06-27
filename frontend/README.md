# Inventory Dashboard Frontend

A modern, responsive Next.js frontend for the Smart Inventory Management Dashboard.

## Features

- **Dashboard**: Real-time metrics, sales analytics, and top-selling products
- **Inventory Management**: Comprehensive product table with inline editing
- **Category Pages**: Filtered views for specific product categories
- **Trends Analysis**: Top and bottom performing products and categories
- **ML Forecasting**: AI-powered demand prediction and recommendations
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Tech Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Interactive charts and graphs
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client for API communication

## Color Palette

The application uses a custom color palette:
- Primary: `#4A4947` (Dark Gray)
- Secondary: `#B17457` (Warm Brown)
- Neutral: `#D8D2C2` (Light Beige)
- Background: `#FAF7F0` (Off White)

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on `http://localhost:8080`

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── components/          # Reusable UI components
│   ├── Layout.tsx      # Main layout with navigation
│   ├── MetricTile.tsx  # Dashboard metric cards
│   ├── ProductTable.tsx # Product data table
│   ├── TrendCharts.tsx # Analytics charts
│   └── ForecastTable.tsx # ML forecast results
├── lib/                # Utilities and API
│   ├── api.ts         # API client and types
│   └── utils.ts       # Helper functions
├── pages/              # Next.js pages
│   ├── index.tsx      # Dashboard home
│   ├── inventory.tsx  # Inventory management
│   ├── trends.tsx     # Performance trends
│   ├── forecast.tsx   # ML forecasting
│   └── category/      # Category-specific pages
└── globals.css        # Global styles and Tailwind
```

## API Integration

The frontend communicates with the Spring Boot backend through REST APIs:

- `GET /api/products` - Get all products
- `PATCH /api/products/{id}` - Update product inventory
- `GET /api/products/category/{id}` - Get products by category
- `POST /api/forecast` - Generate ML forecast

## Features in Detail

### Dashboard
- Real-time metric tiles showing key performance indicators
- Interactive charts for sales analytics
- Top-selling products table with inline editing

### Inventory Management
- Comprehensive product table with search and filtering
- Inline inventory editing with validation
- Status indicators (Low Stock, In Stock, Overstock)

### Category Pages
- Dynamic routing for category-specific views
- Breadcrumb navigation
- Category-scoped product tables

### Trends Analysis
- Top and bottom performing products
- Category performance comparison
- Revenue and product count metrics

### ML Forecasting
- AI-powered demand prediction
- Action recommendations (RESTOCK, DISCOUNT, DEPRECATE, NO ACTION)
- Confidence levels and reasoning
- Action summary dashboard

## Customization

### Colors
Update the color palette in `tailwind.config.js`:

```javascript
colors: {
  primary: { DEFAULT: '#4A4947' },
  secondary: { DEFAULT: '#B17457' },
  neutral: { DEFAULT: '#D8D2C2' },
  background: { DEFAULT: '#FAF7F0' },
}
```

### API Endpoints
Modify the API base URL in `lib/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8080/api';
```

## Development

### Adding New Components
1. Create component file in `components/`
2. Export as default function
3. Import and use in pages

### Adding New Pages
1. Create page file in `pages/`
2. Use the `Layout` component
3. Add navigation item in `components/Layout.tsx`

### Styling
- Use Tailwind CSS classes for styling
- Follow the established color palette
- Use the custom component classes (`.card`, `.btn-primary`, etc.)

## Troubleshooting

### Common Issues

1. **API Connection Errors**: Ensure the backend is running on port 8080
2. **Chart.js Errors**: Install missing dependencies with `npm install`
3. **TypeScript Errors**: Check type definitions and imports

### Performance

- Images are optimized with Next.js Image component
- Charts are lazy-loaded for better performance
- API calls are debounced where appropriate

## Contributing

1. Follow the established code style
2. Use TypeScript for type safety
3. Test components thoroughly
4. Update documentation as needed 
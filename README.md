# Smart Inventory Management Dashboard

A full-stack admin dashboard for warehouse managers to monitor stock levels, predict demand, and get smart recommendations using ML forecasting.

## 🏗️ Architecture

- **Frontend**: Next.js with Tailwind CSS
- **Backend**: Spring Boot (Java, REST API)
- **Database**: PostgreSQL
- **Real-time Signals**: Redis
- **ML Forecasting**: Python (Prophet/ARIMA-ready)

## 🚀 Quick Start

### Prerequisites
- Java 17+
- Node.js 18+
- Python 3.8+
- PostgreSQL
- Redis

### Backend Setup
```bash
cd backend
mvn spring-boot:run
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Database Setup
```bash
# Start PostgreSQL and Redis
# Run the init.sql script in your PostgreSQL instance
```

### ML & Redis Simulation
```bash
cd redis
python cart_simulator.py
```

## 📊 Features

- **Real-time Dashboard**: Monitor stock levels, revenue, and user activity
- **Inventory Management**: Edit stock counts and view product status
- **Category Analytics**: Drill-down into specific product categories
- **Trend Analysis**: Top/bottom performing products and categories
- **ML Forecasting**: AI-powered demand prediction and recommendations
- **Smart Recommendations**: RESTOCK, DISCOUNT, DEPRECATE, NO ACTION

## 🔧 API Endpoints

### Products
- `GET /api/products` - Get all products
- `PATCH /api/products/{id}` - Update product inventory
- `GET /api/products/category/{id}` - Get products by category

### Forecasting
- `POST /api/forecast` - Generate ML forecasts

## 📁 Project Structure

```
admin-inventory/
├── frontend/          # Next.js application
├── backend/           # Spring Boot application
├── ml/               # Python ML scripts
├── redis/            # Redis simulation scripts
└── db/               # Database schema and data
``` 
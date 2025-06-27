import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { 
  Home, 
  Package, 
  TrendingUp, 
  Brain, 
  BarChart3,
  Menu,
  X
} from 'lucide-react';
import { useState } from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Inventory', href: '/inventory', icon: Package },
  { name: 'Trends', href: '/trends', icon: TrendingUp },
  { name: 'Forecast', href: '/forecast', icon: Brain },
];

export default function Layout({ children }: LayoutProps) {
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-50 lg:hidden ${sidebarOpen ? 'block' : 'hidden'}`}>
        <div className="fixed inset-0 bg-black/50" onClick={() => setSidebarOpen(false)} />
        <div className="fixed inset-y-0 left-0 w-64 bg-primary">
          <div className="flex items-center justify-between p-4 border-b border-primary-light">
            <h1 className="text-xl font-bold text-white">Inventory Dashboard</h1>
            <button
              onClick={() => setSidebarOpen(false)}
              className="text-white hover:text-neutral"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
          <nav className="p-4">
            {navigation.map((item) => {
              const isActive = router.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center px-4 py-2 rounded-lg mb-2 transition-colors ${
                    isActive
                      ? 'bg-secondary text-white'
                      : 'text-neutral hover:bg-primary-light hover:text-white'
                  }`}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon className="w-5 h-5 mr-3" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex flex-col flex-grow bg-primary">
          <div className="flex items-center p-4 border-b border-primary-light">
            <h1 className="text-xl font-bold text-white">Inventory Dashboard</h1>
          </div>
          <nav className="flex-1 p-4">
            {navigation.map((item) => {
              const isActive = router.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center px-4 py-2 rounded-lg mb-2 transition-colors ${
                    isActive
                      ? 'bg-secondary text-white'
                      : 'text-neutral hover:bg-primary-light hover:text-white'
                  }`}
                >
                  <item.icon className="w-5 h-5 mr-3" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Header */}
        <header className="bg-background-light border-b border-neutral">
          <div className="flex items-center justify-between px-4 py-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden text-primary hover:text-secondary"
            >
              <Menu className="w-6 h-6" />
            </button>
            <div className="flex items-center space-x-4">
              <BarChart3 className="w-6 h-6 text-secondary" />
              <h2 className="text-lg font-semibold text-primary">Smart Inventory Management</h2>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  );
} 
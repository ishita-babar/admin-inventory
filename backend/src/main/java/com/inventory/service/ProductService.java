package com.inventory.service;

import com.inventory.dto.ProductDTO;
import com.inventory.model.Product;
import com.inventory.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Transactional
public class ProductService {
    
    @Autowired
    private ProductRepository productRepository;
    
    /**
     * Get all products
     */
    public List<ProductDTO> getAllProducts() {
        List<Product> products = productRepository.findAll();
        return products.stream()
                .map(ProductDTO::new)
                .collect(Collectors.toList());
    }
    
    /**
     * Get product by ID
     */
    public Optional<ProductDTO> getProductById(Long id) {
        Optional<Product> product = productRepository.findById(id);
        return product.map(ProductDTO::new);
    }
    
    /**
     * Get products by category ID
     */
    public List<ProductDTO> getProductsByCategory(Long categoryId) {
        List<Product> products = productRepository.findByCategoryIdWithCategory(categoryId);
        return products.stream()
                .map(ProductDTO::new)
                .collect(Collectors.toList());
    }
    
    /**
     * Update product inventory
     */
    public Optional<ProductDTO> updateInventory(Long productId, Integer newInventoryCount) {
        Optional<Product> productOpt = productRepository.findById(productId);
        
        if (productOpt.isPresent()) {
            Product product = productOpt.get();
            product.setInventoryCount(newInventoryCount);
            Product savedProduct = productRepository.save(product);
            return Optional.of(new ProductDTO(savedProduct));
        }
        
        return Optional.empty();
    }
    
    /**
     * Get low stock products
     */
    public List<ProductDTO> getLowStockProducts() {
        List<Product> products = productRepository.findLowStockProducts();
        return products.stream()
                .map(ProductDTO::new)
                .collect(Collectors.toList());
    }
    
    /**
     * Get overstock products
     */
    public List<ProductDTO> getOverstockProducts() {
        List<Product> products = productRepository.findOverstockProducts();
        return products.stream()
                .map(ProductDTO::new)
                .collect(Collectors.toList());
    }
    
    /**
     * Get product by SKU
     */
    public Optional<ProductDTO> getProductBySku(String sku) {
        Product product = productRepository.findBySku(sku);
        return Optional.ofNullable(product).map(ProductDTO::new);
    }
    
    /**
     * Get total product count
     */
    public long getTotalProductCount() {
        return productRepository.count();
    }
    
    /**
     * Get total inventory count
     */
    public Integer getTotalInventoryCount() {
        List<Product> products = productRepository.findAll();
        return products.stream()
                .mapToInt(Product::getInventoryCount)
                .sum();
    }
    
    /**
     * Get paginated products
     */
    public Page<ProductDTO> getPaginatedProducts(Pageable pageable) {
        return productRepository.findAll(pageable).map(ProductDTO::new);
    }
} 
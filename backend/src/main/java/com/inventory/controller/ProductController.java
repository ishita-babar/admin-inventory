package com.inventory.controller;

import com.inventory.dto.InventoryUpdateDTO;
import com.inventory.dto.ProductDTO;
import com.inventory.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/products")
@CrossOrigin(origins = "http://localhost:3000")
public class ProductController {
    
    @Autowired
    private ProductService productService;
    
    /**
     * GET /api/products - Get all products
     */
    @GetMapping
    public ResponseEntity<List<ProductDTO>> getAllProducts() {
        List<ProductDTO> products = productService.getAllProducts();
        return ResponseEntity.ok(products);
    }
    
    /**
     * GET /api/products/{id} - Get product by ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<ProductDTO> getProductById(@PathVariable Long id) {
        return productService.getProductById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * PATCH /api/products/{id} - Update product inventory
     */
    @PatchMapping("/{id}")
    public ResponseEntity<ProductDTO> updateInventory(
            @PathVariable Long id,
            @Valid @RequestBody InventoryUpdateDTO updateDTO) {
        
        return productService.updateInventory(id, updateDTO.getInventoryCount())
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * GET /api/products/category/{id} - Get products by category
     */
    @GetMapping("/category/{categoryId}")
    public ResponseEntity<List<ProductDTO>> getProductsByCategory(@PathVariable Long categoryId) {
        List<ProductDTO> products = productService.getProductsByCategory(categoryId);
        return ResponseEntity.ok(products);
    }
    
    /**
     * GET /api/products/sku/{sku} - Get product by SKU
     */
    @GetMapping("/sku/{sku}")
    public ResponseEntity<ProductDTO> getProductBySku(@PathVariable String sku) {
        return productService.getProductBySku(sku)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * GET /api/products/low-stock - Get low stock products
     */
    @GetMapping("/low-stock")
    public ResponseEntity<List<ProductDTO>> getLowStockProducts() {
        List<ProductDTO> products = productService.getLowStockProducts();
        return ResponseEntity.ok(products);
    }
    
    /**
     * GET /api/products/overstock - Get overstock products
     */
    @GetMapping("/overstock")
    public ResponseEntity<List<ProductDTO>> getOverstockProducts() {
        List<ProductDTO> products = productService.getOverstockProducts();
        return ResponseEntity.ok(products);
    }
    
    /**
     * GET /api/products/stats - Get product statistics
     */
    @GetMapping("/stats")
    public ResponseEntity<Map<String, Object>> getProductStats() {
        Map<String, Object> stats = Map.of(
            "totalProducts", productService.getTotalProductCount(),
            "totalInventory", productService.getTotalInventoryCount(),
            "lowStockCount", productService.getLowStockProducts().size(),
            "overstockCount", productService.getOverstockProducts().size()
        );
        return ResponseEntity.ok(stats);
    }
    
    /**
     * GET /api/products/page - Get paginated products
     */
    @GetMapping("/page")
    public ResponseEntity<Page<ProductDTO>> getPaginatedProducts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<ProductDTO> products = productService.getPaginatedProducts(pageable);
        return ResponseEntity.ok(products);
    }
} 
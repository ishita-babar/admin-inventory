package com.inventory.dto;

import com.inventory.model.Product;
import java.math.BigDecimal;

public class ProductDTO {
    private Long id;
    private String sku;
    private String name;
    private String description;
    private CategoryDTO category;
    private BigDecimal price;
    private Integer inventoryCount;
    private Integer minStockLevel;
    private Integer maxStockLevel;
    private String inventoryStatus;
    
    // Constructors
    public ProductDTO() {}
    
    public ProductDTO(Product product) {
        this.id = product.getId();
        this.sku = product.getSku();
        this.name = product.getName();
        this.description = product.getDescription();
        this.category = product.getCategory() != null ? new CategoryDTO(product.getCategory()) : null;
        this.price = product.getPrice();
        this.inventoryCount = product.getInventoryCount();
        this.minStockLevel = product.getMinStockLevel();
        this.maxStockLevel = product.getMaxStockLevel();
        this.inventoryStatus = product.getInventoryStatus();
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getSku() {
        return sku;
    }
    
    public void setSku(String sku) {
        this.sku = sku;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public CategoryDTO getCategory() {
        return category;
    }
    
    public void setCategory(CategoryDTO category) {
        this.category = category;
    }
    
    public BigDecimal getPrice() {
        return price;
    }
    
    public void setPrice(BigDecimal price) {
        this.price = price;
    }
    
    public Integer getInventoryCount() {
        return inventoryCount;
    }
    
    public void setInventoryCount(Integer inventoryCount) {
        this.inventoryCount = inventoryCount;
    }
    
    public Integer getMinStockLevel() {
        return minStockLevel;
    }
    
    public void setMinStockLevel(Integer minStockLevel) {
        this.minStockLevel = minStockLevel;
    }
    
    public Integer getMaxStockLevel() {
        return maxStockLevel;
    }
    
    public void setMaxStockLevel(Integer maxStockLevel) {
        this.maxStockLevel = maxStockLevel;
    }
    
    public String getInventoryStatus() {
        return inventoryStatus;
    }
    
    public void setInventoryStatus(String inventoryStatus) {
        this.inventoryStatus = inventoryStatus;
    }
} 
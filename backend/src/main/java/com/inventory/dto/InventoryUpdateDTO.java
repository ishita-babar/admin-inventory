package com.inventory.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public class InventoryUpdateDTO {
    
    @NotNull(message = "Inventory count is required")
    @Min(value = 0, message = "Inventory count must be non-negative")
    private Integer inventoryCount;
    
    // Constructors
    public InventoryUpdateDTO() {}
    
    public InventoryUpdateDTO(Integer inventoryCount) {
        this.inventoryCount = inventoryCount;
    }
    
    // Getters and Setters
    public Integer getInventoryCount() {
        return inventoryCount;
    }
    
    public void setInventoryCount(Integer inventoryCount) {
        this.inventoryCount = inventoryCount;
    }
} 
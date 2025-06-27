package com.inventory.service;

import com.inventory.model.Category;
import com.inventory.model.Product;
import com.inventory.repository.CategoryRepository;
import com.inventory.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;

import jakarta.annotation.PostConstruct;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

@Component
public class ProductDataLoader {
    @Autowired
    private ProductRepository productRepository;
    @Autowired
    private CategoryRepository categoryRepository;

    @PostConstruct
    public void loadProductsFromCSV() {
        try {
            ClassPathResource resource = new ClassPathResource("products.csv");
            BufferedReader reader = new BufferedReader(new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8));
            String line;
            boolean first = true;
            Map<String, Category> categoryCache = new HashMap<>();
            while ((line = reader.readLine()) != null) {
                if (first) { first = false; continue; } // skip header
                String[] fields = line.split(",");
                if (fields.length < 7) continue;
                String sku = fields[0].trim();
                String name = fields[1].trim();
                String categoryName = fields[2].trim();
                int unitsInStock = Integer.parseInt(fields[3].trim());
                BigDecimal price = new BigDecimal(fields[4].trim());
                // rating_avg and return_rate are ignored for now

                // Check if product already exists by SKU
                if (productRepository.findBySku(sku) != null) continue;

                // Find or create category
                Category category = categoryCache.get(categoryName);
                if (category == null) {
                    category = categoryRepository.findByName(categoryName);
                    if (category == null) {
                        category = new Category();
                        category.setName(categoryName);
                        category.setDescription(categoryName + " products");
                        category = categoryRepository.save(category);
                    }
                    categoryCache.put(categoryName, category);
                }

                Product product = new Product();
                product.setSku(sku);
                product.setName(name);
                product.setCategory(category);
                product.setPrice(price);
                product.setInventoryCount(unitsInStock);
                productRepository.save(product);
            }
            reader.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
} 
package com.inventory.service;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

@Service
public class ForecastService {
    
    @Value("${ml.script-path}")
    private String scriptPath;
    
    @Value("${ml.python-command}")
    private String pythonCommand;
    
    private final ObjectMapper objectMapper = new ObjectMapper();
    
    /**
     * Generate forecast by reading from ml/forecast_output.json
     */
    public List<Map<String, Object>> generateForecast() {
        try {
            System.out.println("Current working directory: " + new java.io.File(".").getAbsolutePath());
            System.out.println("Looking for: " + new java.io.File("ml/forecast_output.json").getAbsolutePath());
            String jsonOutput = new String(Files.readAllBytes(Paths.get("/Users/ishita/admin-inventory/ml/forecast_output.json")));
            System.out.println("DEBUG: Raw JSON output: " + jsonOutput);
            return objectMapper.readValue(jsonOutput, new TypeReference<List<Map<String, Object>>>() {});
        } catch (com.fasterxml.jackson.core.JsonProcessingException e) {
            e.printStackTrace();
            throw new RuntimeException("Failed to parse forecast JSON: " + e.getMessage(), e);
        } catch (java.io.IOException e) {
            e.printStackTrace();
            throw new RuntimeException("Failed to read forecast JSON file: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get forecast status
     */
    public Map<String, Object> getForecastStatus() {
        return Map.of(
            "status", "ready",
            "script_path", scriptPath,
            "python_command", pythonCommand
        );
    }
} 
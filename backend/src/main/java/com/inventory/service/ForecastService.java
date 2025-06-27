package com.inventory.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.List;
import java.util.Map;

@Service
public class ForecastService {
    
    @Value("${ml.script-path}")
    private String scriptPath;
    
    @Value("${ml.python-command}")
    private String pythonCommand;
    
    private final ObjectMapper objectMapper = new ObjectMapper();
    
    /**
     * Generate forecast using ML script
     */
    public List<Map<String, Object>> generateForecast() {
        try {
            // Build the command to execute the Python script
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonCommand, scriptPath
            );
            
            // Set working directory to the script location
            processBuilder.directory(new java.io.File(scriptPath).getParentFile());
            
            // Redirect error stream to output stream
            processBuilder.redirectErrorStream(true);
            
            // Start the process
            Process process = processBuilder.start();
            
            // Read the output
            BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream())
            );
            
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            
            // Wait for the process to complete
            int exitCode = process.waitFor();
            
            if (exitCode == 0) {
                // Parse the JSON output
                String jsonOutput = output.toString().trim();
                return objectMapper.readValue(jsonOutput, new TypeReference<List<Map<String, Object>>>() {});
            } else {
                throw new RuntimeException("ML script failed with exit code: " + exitCode);
            }
            
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate forecast: " + e.getMessage(), e);
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
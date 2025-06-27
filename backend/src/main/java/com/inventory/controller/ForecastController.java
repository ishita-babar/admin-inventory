package com.inventory.controller;

import com.inventory.service.ForecastService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/forecast")
@CrossOrigin(origins = "http://localhost:3000")
public class ForecastController {
    
    @Autowired
    private ForecastService forecastService;
    
    /**
     * POST /api/forecast - Generate ML forecast
     */
    @PostMapping
    public ResponseEntity<List<Map<String, Object>>> generateForecast() {
        try {
            List<Map<String, Object>> forecast = forecastService.generateForecast();
            return ResponseEntity.ok(forecast);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }
    
    /**
     * GET /api/forecast/status - Get forecast service status
     */
    @GetMapping("/status")
    public ResponseEntity<Map<String, Object>> getForecastStatus() {
        Map<String, Object> status = forecastService.getForecastStatus();
        return ResponseEntity.ok(status);
    }
} 
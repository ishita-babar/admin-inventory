package com.inventory.controller;

import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.CrossOrigin;

import com.inventory.service.ForecastService;

@RestController
@RequestMapping("/api/forecast")
@CrossOrigin(origins = "http://localhost:3000")
public class ForecastController {

    private static final Logger logger = LoggerFactory.getLogger(ForecastController.class);

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
            logger.error("Error generating forecast", e); // Log the full error/stack trace
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
import csv
import os
from datetime import datetime, timedelta
from fastapi import HTTPException
from .logger import CustomLogger

class Monitor:
    def __init__(self):
        self.logs = []
        self.logger = CustomLogger("Monitor")
    
    def log_request(self, module, api, status_code, latency):
        timestamp = datetime.now()
        self.logs.append({
            "timestamp": timestamp,
            "module": module,
            "api": api,
            "status_code": status_code,
            "latency": latency
        })
        self.logger.log(api, "log_request", 
                       f"Request logged | Status: {status_code} | Latency: {latency}ms")
    
    def get_latency(self, module, start_date, end_date):
        start_time = time.time()
        filtered = [log for log in self.logs 
                   if log["module"] == module 
                   and start_date <= log["timestamp"] <= end_date]
        
        if not filtered:
            return None
        
        avg_latency = sum(log["latency"] for log in filtered) / len(filtered)
        self.logger.log("Monitor", "get_latency", 
                       f"Latency calculated for {module}", start_time)
        return avg_latency
    
    def get_availability(self, module, days):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        filtered = [log for log in self.logs 
                   if log["module"] == module 
                   and start_date <= log["timestamp"] <= end_date]
        
        if not filtered:
            return None
        
        success = sum(1 for log in filtered if log["status_code"] == 200)
        errors = sum(1 for log in filtered if log["status_code"] == 500)
        
        availability = (success / (success + errors)) * 100 if (success + errors) > 0 else 0
        return availability

monitor = Monitor()
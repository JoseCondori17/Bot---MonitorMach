import re
from datetime import datetime, timedelta
from collections import defaultdict
import math

class BotAnalyzer:
    def __init__(self, log_file="logs/monitoring.log"):
        self.log_file = log_file
        self.logs = self._parse_logs()
    
    def _parse_logs(self):
        """Extrae datos estructurados del archivo de log con el nuevo formato"""
        logs = []
        log_pattern = re.compile(
            r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\|'
            r'(?P<module>[^|]+)\|'
            r'(?P<submodule>[^|]+)\|'
            r'(?P<function>[^|]+)\|'
            r'(?P<message>.*)'
        )
        
        with open(self.log_file, 'r') as f:
            for line in f:
                match = log_pattern.match(line.strip())
                if match:
                    log_data = match.groupdict()
                    # Extraer información adicional del mensaje
                    latency_match = re.search(r'Latency: (\d+)ms', log_data['message'])
                    status_match = re.search(r'Status: (\d+)', log_data['message'])
                    
                    log_entry = {
                        'timestamp': datetime.strptime(log_data['timestamp'], "%Y-%m-%d %H:%M:%S"),
                        'module': log_data['module'],
                        'submodule': log_data['submodule'],
                        'function': log_data['function'],
                        'message': log_data['message'],
                        'latency': int(latency_match.group(1)) if latency_match else 0,
                        'status': int(status_match.group(1)) if status_match else 200
                    }
                    logs.append(log_entry)
        return logs
    
    def _filter_logs(self, module=None, start_date=None, end_date=None, function=None):
        """Filtra logs según criterios"""
        filtered = self.logs
        
        if module:
            filtered = [log for log in filtered if log['module'] == module]
        if function:
            filtered = [log for log in filtered if log['function'] == function]
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            filtered = [log for log in filtered if log['timestamp'] >= start_date]
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            filtered = [log for log in filtered if log['timestamp'] < end_date]
            
        return filtered
    
    def check_latency(self, module=None, start_date=None, end_date=None, function=None):
        """Muestra la latencia de la aplicación para un módulo en un periodo"""
        filtered = self._filter_logs(module, start_date, end_date, function)
        
        if not filtered:
            return "No hay datos para los criterios especificados"
            
        # Agrupar por día
        daily_data = defaultdict(list)
        for log in filtered:
            date_str = log['timestamp'].strftime("%m/%d")
            daily_data[date_str].append(log['latency'])
        
        # Calcular promedios diarios
        results = []
        for date, latencies in sorted(daily_data.items()):
            avg_latency = sum(latencies) / len(latencies)
            results.append(f"{date} {avg_latency:.0f}ms")
        
        header = f"Latency report for {module or 'all modules'}"
        if function:
            header += f" (function: {function})"
        if start_date and end_date:
            header += f" from {start_date} to {end_date}"
        
        return "\n".join([header] + results)
    
    def check_availability(self, module=None, days=7, function=None):
        """Muestra la disponibilidad del servicio durante X días"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        filtered = self._filter_logs(
            module=module,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            function=function
        )
        
        if not filtered:
            return "No hay datos para los criterios especificados"
            
        # Agrupar por día
        daily_data = defaultdict(lambda: {'success': 0, 'errors': 0})
        for log in filtered:
            date_str = log['timestamp'].strftime("%m/%d")
            if log['status'] == 200:
                daily_data[date_str]['success'] += 1
            else:
                daily_data[date_str]['errors'] += 1
        
        # Calcular disponibilidad diaria
        results = []
        for date in sorted(daily_data.keys()):
            data = daily_data[date]
            total = data['success'] + data['errors']
            availability = (data['success'] / total) * 100 if total > 0 else 0
            results.append(f"{date} {availability:.1f}% (Success: {data['success']}, Errors: {data['errors']})")
        
        header = f"Availability report for {module or 'all modules'} - Last {days} days"
        if function:
            header += f" (function: {function})"
        
        return "\n".join([header] + results)
    
    def render_graph(self, metric="latency", module=None, days=7, function=None, height=10):
        """Renderiza una gráfica ASCII de las tendencias"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Obtener datos según la métrica
        if metric.lower() == "latency":
            filtered = self._filter_logs(
                module=module,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                function=function
            )
            
            # Agrupar por día y calcular promedio
            daily_data = defaultdict(list)
            for log in filtered:
                date_str = log['timestamp'].strftime("%m/%d")
                daily_data[date_str].append(log['latency'])
            
            dates = sorted(daily_data.keys())
            values = [sum(daily_data[date])/len(daily_data[date]) for date in dates]
            title = f"Latency Trend for {module or 'all modules'}"
            
        elif metric.lower() == "availability":
            filtered = self._filter_logs(
                module=module,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                function=function
            )
            
            # Agrupar por día y calcular disponibilidad
            daily_data = defaultdict(lambda: {'success': 0, 'errors': 0})
            for log in filtered:
                date_str = log['timestamp'].strftime("%m/%d")
                if log['status'] == 200:
                    daily_data[date_str]['success'] += 1
                else:
                    daily_data[date_str]['errors'] += 1
            
            dates = sorted(daily_data.keys())
            values = []
            for date in dates:
                data = daily_data[date]
                total = data['success'] + data['errors']
                availability = (data['success'] / total) * 100 if total > 0 else 0
                values.append(availability)
            title = f"Availability Trend for {module or 'all modules'}"
        
        else:
            return "Métrica no válida. Use 'latency' o 'availability'"
        
        if not dates:
            return "No hay datos para mostrar el gráfico"
        
        # Normalizar valores para la altura del gráfico
        max_val = max(values)
        min_val = min(values)
        range_val = max_val - min_val if max_val != min_val else 1
        
        scaled_values = [int((val - min_val) / range_val) * height for val in values]
        
        # Construir gráfico ASCII
        graph_lines = []
        for level in range(height, -1, -1):
            line = []
            for val in scaled_values:
                if val >= level:
                    line.append("***")
                else:
                    line.append("   ")
            graph_lines.append(" ".join(line))
        
        # Añadir ejes
        date_line = "  ".join(dates)
        value_line = f"Min: {min_val:.1f}{'ms' if metric == 'latency' else '%'}  Max: {max_val:.1f}{'ms' if metric == 'latency' else '%'}"
        
        return "\n".join([title] + graph_lines + [date_line, value_line])


# Interfaz de usuario simple
if __name__ == "__main__":
    analyzer = BotAnalyzer()
    
    print("=== Bot Analyzer ===")
    print("1. Check Latency")
    print("2. Check Availability")
    print("3. Render Graph")
    print("4. Exit")
    
    while True:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            module = input("Enter module name (optional): ").strip() or None
            start = input("Enter start date (YYYY-MM-DD, optional): ").strip() or None
            end = input("Enter end date (YYYY-MM-DD, optional): ").strip() or None
            func = input("Enter function name (optional): ").strip() or None
            print("\n" + analyzer.check_latency(module, start, end, func))
            
        elif choice == "2":
            module = input("Enter module name (optional): ").strip() or None
            days = input("Enter number of days (default 7): ").strip() or "7"
            func = input("Enter function name (optional): ").strip() or None
            print("\n" + analyzer.check_availability(module, int(days), func))
            
        elif choice == "3":
            metric = input("Enter metric (latency/availability): ").strip().lower()
            module = input("Enter module name (optional): ").strip() or None
            days = input("Enter number of days (default 7): ").strip() or "7"
            func = input("Enter function name (optional): ").strip() or None
            print("\n" + analyzer.render_graph(metric, module, int(days), func))
            
        elif choice == "4":
            print("Exiting...")
            break
            
        else:
            print("Invalid choice. Please select 1-4.")
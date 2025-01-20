import psutil
import time
import csv
from datetime import datetime
from flask import Flask, jsonify, request
import threading
import os
import json

app = Flask(__name__)

class SystemMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.monitor_thread = None
        self.current_test_info = None
        
    def get_output_file(self):
        # Create filename based on test metadata
        if self.current_test_info:
            tag = self.current_test_info.get('tag', 'notag')
            custom_arg = self.current_test_info.get('custom_arg', 'default')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return f"system_metrics_{tag}_{custom_arg}_{timestamp}.csv"
        return "system_metrics_default.csv"
        
    def collect_metrics(self):
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'swap_percent': psutil.swap_memory().percent,
            'disk_usage_percent': psutil.disk_usage('/').percent,
            'network_bytes_sent': psutil.net_io_counters().bytes_sent,
            'network_bytes_recv': psutil.net_io_counters().bytes_recv
        }
        
        # Add test metadata to metrics
        if self.current_test_info:
            metrics.update({
                'test_tag': self.current_test_info.get('tag'),
                'custom_arg': self.current_test_info.get('custom_arg'),
                'host': self.current_test_info.get('host'),
                'user_count': self.current_test_info.get('user_count')
            })
            
        return metrics
    
    def write_header(self, filename):
        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                headers = ['timestamp', 'cpu_percent', 'memory_percent', 
                          'swap_percent', 'disk_usage_percent',
                          'network_bytes_sent', 'network_bytes_recv']
                if self.current_test_info:
                    headers.extend(['test_tag', 'custom_arg', 'host', 'user_count'])
                writer.writerow(headers)
    
    def monitor(self):
        output_file = self.get_output_file()
        self.write_header(output_file)
        
        while self.is_monitoring:
            metrics = self.collect_metrics()
            with open(output_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(metrics.values())
            time.sleep(1)
    
    def start(self, test_info):
        if not self.is_monitoring:
            self.current_test_info = test_info
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor)
            self.monitor_thread.start()
    
    def stop(self):
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        self.current_test_info = None

system_monitor = SystemMonitor()

@app.route('/monitor/start', methods=['POST'])
def start_monitoring():
    test_info = request.get_json()
    system_monitor.start(test_info)
    return jsonify({
        'status': 'Monitoring started',
        'test_info': test_info
    })

@app.route('/monitor/stop', methods=['POST'])
def stop_monitoring():
    system_monitor.stop()
    return jsonify({'status': 'Monitoring stopped'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

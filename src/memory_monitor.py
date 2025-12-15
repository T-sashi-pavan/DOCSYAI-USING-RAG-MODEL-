"""
Memory monitoring utilities for 500MB cloud deployment.
Add this to your monitoring dashboard.
"""

import os
import time
from typing import Dict

class MemoryMonitor:
    """Monitor memory usage during PDF processing."""
    
    def __init__(self):
        self.start_memory = 0
        self.peak_memory = 0
        self.current_memory = 0
    
    def get_memory_mb(self) -> float:
        """Get current memory usage in MB."""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            # Fallback if psutil not available
            return 0
    
    def start_tracking(self) -> float:
        """Start memory tracking."""
        self.start_memory = self.get_memory_mb()
        self.peak_memory = self.start_memory
        self.current_memory = self.start_memory
        return self.start_memory
    
    def check_memory(self) -> Dict[str, float]:
        """Get memory stats."""
        self.current_memory = self.get_memory_mb()
        
        if self.current_memory > self.peak_memory:
            self.peak_memory = self.current_memory
        
        return {
            'current_mb': round(self.current_memory, 2),
            'peak_mb': round(self.peak_memory, 2),
            'delta_mb': round(self.current_memory - self.start_memory, 2),
            'available_mb': 500 - self.peak_memory,
            'utilization': round((self.peak_memory / 500) * 100, 1)
        }
    
    def get_stats(self) -> Dict:
        """Get complete memory statistics."""
        stats = self.check_memory()
        stats['status'] = 'OK' if stats['available_mb'] > 50 else 'WARNING'
        return stats
    
    @staticmethod
    def warn_if_high() -> bool:
        """Return True if memory usage is high."""
        monitor = MemoryMonitor()
        current = monitor.get_memory_mb()
        
        if current > 400:  # 400MB out of 500MB
            print(f"⚠️  HIGH MEMORY WARNING: {current:.1f}MB / 500MB")
            return True
        
        return False


# Example usage:
if __name__ == "__main__":
    try:
        import psutil
        print("✓ Memory monitoring available")
        
        monitor = MemoryMonitor()
        monitor.start_tracking()
        
        print(f"📊 Memory Stats:")
        stats = monitor.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
    
    except ImportError:
        print("⚠️  psutil not installed")
        print("   Install: pip install psutil")
        print("   For memory monitoring in cloud")

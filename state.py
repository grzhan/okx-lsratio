import threading
import copy
from datetime import datetime

class GlobalState:
    """
    线程安全的全局状态管理单例
    """
    _instance = None
    _lock = threading.Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(GlobalState, cls).__new__(cls)
                cls._instance.subscriptions = set()
                cls._instance._state_lock = threading.Lock()
                cls._instance.alerted = {}
        return cls._instance

    def subscribe(self, target: str):
        with self._state_lock:
            self.subscriptions.add(target)

    def unsubscribe(self, target: str):
        with self._state_lock:
            self.subscriptions.remove(target)
    
    def get_subscriptions(self):
        with self._state_lock:
            return copy.deepcopy(self.subscriptions)
    
    def mark_as_alerted(self, target: str):
        with self._state_lock:
            self.alerted[target] = datetime.now().strftime('%Y-%m-%d')

    def check_if_alerted(self, target: str):
        with self._state_lock:
            if target not in self.alerted:
                return False
            return self.alerted[target] == datetime.now().strftime('%Y-%m-%d')

    def clear_alert_record(self):
        with self._state_lock:
            self.alerted = {}


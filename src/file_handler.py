import time
import logging
import watchdog.events
from watchdog.observers import Observer


class KrytonFileEventHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, callback, time_window_ms=20):
        self.callback = callback
        self.stack = {}
        self.time_window_ms = time_window_ms
        super().__init__()

    def execute_callback(self, event):
        if self.callback and callable(self.callback):
            ms = int(round(time.time() * 1000))
            uid = f"{event.event_type}-{event.src_path}"

            if uid in self.stack:
                time_diff = round(ms - self.stack[uid])
                if time_diff < self.time_window_ms:
                    return

            self.stack[uid] = ms
            logging.debug(f"File change: {event.src_path}")
            self.callback(event)

    def on_created(self, event):
        self.execute_callback(event)

    def on_modified(self, event):
        self.execute_callback(event)


class KrytonFileObserver:
    def __init__(self, path, event_callback):
        logging.info(f"File observer path: {path}")
        self.observer = Observer()
        self.file_handler = KrytonFileEventHandler(event_callback)
        self.observer.schedule(self.file_handler, path, recursive=True)
        self.observer.start()
        logging.info(f"File observer - START")

    def stop(self):
        self.observer.stop()
        logging.info(f"File observer - STOP")

    def join(self):
        self.observer.join()
        logging.info(f"File observer - JOIN")

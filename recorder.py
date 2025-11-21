#!/usr/bin/python
import subprocess
import datetime
import os
import sys
import time
import signal
import logging
from threading import Thread
from config import *
from gpio_controller import GPIOController
from scanner_reader import ScannerReader

os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/recorder.log"),
        logging.StreamHandler()
    ]
)

class Recorder:
    def __init__(self):
        self.current_order = None
        self.recording_proc = None
        self.last_scan_time = 0
        
        try:
            self.gpio = GPIOController(LED_PIN, BUTTON_PIN, self.stop_recording)
            logging.info("GPIO initialized")
        except Exception as e:
            logging.warning(f"GPIO failed: {e}. Running without button/LED.")
            self.gpio = None
        
        self.scanner = ScannerReader(SCANNER_DEVICE)
        
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
    
    def next_video_filename(self, order):
        today = datetime.date.today().strftime("%Y-%m-%d")
        folder = os.path.join(VIDEO_BASE_DIR, today)
        os.makedirs(folder, exist_ok=True)
        
        base = os.path.join(folder, f"{order}.mp4")
        if not os.path.exists(base):
            return base
        
        counter = 2
        while os.path.exists(os.path.join(folder, f"{order}_{counter}.mp4")):
            counter += 1
        return os.path.join(folder, f"{order}_{counter}.mp4")
    
    def start_recording(self, order):
        outfile = self.next_video_filename(order)
        cmd = FFMPEG_CMD + [outfile]
        
        logging.info(f"START: {outfile}")
        self.recording_proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if self.gpio:
            self.gpio.led_on()
    
    def stop_recording(self):
        if self.recording_proc:
            logging.info("STOP")
            self.recording_proc.terminate()
            Thread(target=lambda: self.recording_proc.wait(5), daemon=True).start()
            self.recording_proc = None
            self.current_order = None
            if self.gpio:
                self.gpio.led_off()
    
    def handle_scan(self, code):
        now = time.time()
        if now - self.last_scan_time < SCAN_COOLDOWN:
            return
        
        if not code.startswith(QR_PREFIXES):
            return
        
        self.last_scan_time = now
        
        if self.recording_proc is None:
            self.current_order = code
            self.start_recording(code)
        elif code == self.current_order:
            self.stop_recording()
    
    def run(self):
        logging.info("Ready")
        self.scanner.read_codes(self.handle_scan)
    
    def shutdown(self, *args):
        logging.info("Shutdown")
        self.stop_recording()
        if self.gpio:
            self.gpio.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    Recorder().run()
VIDEO_BASE_DIR = "/home/pi/videos"
LOG_DIR = "/home/pi/logs"

LED_PIN = 17
BUTTON_PIN = 27

QR_PREFIXES = ("CA-", "US-")

# Your scanner device
SCANNER_DEVICE = "/dev/input/by-id/usb-Linux_4.9.84_Aigather_Scan-event-kbd"

FFMPEG_CMD = [
    "ffmpeg", "-f", "v4l2",
    "-input_format", "mjpeg",
    "-framerate", "30",
    "-video_size", "1280x720",
    "-i", "/dev/video0",
    "-c:v", "copy"
]

SCAN_COOLDOWN = 2.0
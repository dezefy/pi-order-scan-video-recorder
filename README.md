# Pi Order Scan Video Recorder

A Raspberry Pi-based video recording system that automatically captures footage when order/package QR codes are scanned. Perfect for documenting order packaging processes, quality control, or shipping verification.

## Features

- **QR Code Triggered Recording** - Scan a QR code to start recording, scan again to stop
- **Order-Based File Naming** - Videos are automatically named after the scanned order code
- **Date-Organized Storage** - Recordings are sorted into daily folders
- **LED Status Indicator** - Visual feedback when recording is active
- **Manual Stop Button** - Hardware button to stop recording without rescanning
- **Auto-Restart Service** - Runs as a systemd service with automatic recovery
- **Debounce Protection** - 2-second cooldown prevents accidental double-scans

## Hardware Requirements

- Raspberry Pi (tested on Pi 3/4)
- USB Webcam (v4l2 compatible)
- USB QR/Barcode Scanner (HID keyboard mode)
- LED (connected to GPIO 17)
- Push button (connected to GPIO 27)

### Wiring Diagram

```
LED:
  - Positive (long leg) → GPIO 17
  - Negative (short leg) → GND (with appropriate resistor)

Button:
  - One terminal → GPIO 27
  - Other terminal → GND
```

## Installation

### Prerequisites

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip ffmpeg python3-evdev
```

### Setup

1. Clone the repository:
```bash
git clone https://github.com/dezefy/pi-order-scan-video-recorder.git
cd pi-order-scan-video-recorder
```

2. Copy files to the Pi:
```bash
mkdir -p /home/pi/recorder
cp *.py /home/pi/recorder/
cp recorder.service /home/pi/recorder/
```

3. Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

## Configuration

Edit `config.py` to customize settings:

```python
# Storage locations
VIDEO_BASE_DIR = "/home/pi/videos"
LOG_DIR = "/home/pi/logs"

# GPIO pins (BCM numbering)
LED_PIN = 17
BUTTON_PIN = 27

# Valid QR code prefixes (modify for your order codes)
QR_PREFIXES = ("CA-", "US-")

# Scanner device path (find yours with: ls /dev/input/by-id/)
SCANNER_DEVICE = "/dev/input/by-id/usb-Linux_4.9.84_Aigather_Scan-event-kbd"

# Video settings
FFMPEG_CMD = [
    "ffmpeg", "-f", "v4l2",
    "-input_format", "mjpeg",
    "-framerate", "30",
    "-video_size", "1280x720",
    "-i", "/dev/video0",
    "-c:v", "copy"
]

# Minimum time between scans (seconds)
SCAN_COOLDOWN = 2.0
```

### Finding Your Scanner Device

```bash
ls /dev/input/by-id/
```

Look for a device with "kbd" in the name - that's your scanner in keyboard mode.

### Finding Your Camera Device

```bash
ls /dev/video*
v4l2-ctl --list-devices
```

## Usage

### Manual Start

```bash
python3 /home/pi/recorder/recorder.py
```

### Service Management

```bash
# Check status
sudo systemctl status recorder

# View logs
journalctl -u recorder -f

# Restart service
sudo systemctl restart recorder

# Stop service
sudo systemctl stop recorder
```

### Recording Workflow

1. **Start Recording**: Scan an order QR code (e.g., "CA-12345")
   - LED turns ON
   - Video file created: `/home/pi/videos/YYYY-MM-DD/CA-12345.mp4`

2. **Stop Recording**: Either:
   - Scan the same QR code again, OR
   - Press the hardware button
   - LED turns OFF

3. **Multiple Takes**: Scanning the same order again creates numbered versions:
   - `CA-12345.mp4`
   - `CA-12345_2.mp4`
   - `CA-12345_3.mp4`

## File Structure

```
/home/pi/
├── recorder/
│   ├── recorder.py          # Main application
│   ├── config.py             # Configuration settings
│   ├── gpio_controller.py    # LED and button control
│   ├── scanner_reader.py     # QR scanner input handler
│   └── recorder.service      # Systemd service file
├── videos/
│   ├── 2024-01-15/
│   │   ├── CA-12345.mp4
│   │   └── US-67890.mp4
│   └── 2024-01-16/
│       └── CA-11111.mp4
└── logs/
    └── recorder.log
```

## Troubleshooting

### Scanner not detected

```bash
# Check if scanner is recognized
lsusb

# Check input devices
ls /dev/input/by-id/

# Test scanner input
cat /dev/input/by-id/your-scanner-device
```

### Camera not working

```bash
# List cameras
v4l2-ctl --list-devices

# Test camera
ffmpeg -f v4l2 -i /dev/video0 -frames 1 test.jpg
```

### GPIO issues

```bash
# Test GPIO with included script
python3 test_gpio.py

# Check GPIO permissions
groups $USER  # Should include 'gpio'
```

### Service won't start

```bash
# Check detailed logs
journalctl -u recorder -n 50

# Verify file permissions
ls -la /home/pi/recorder/
```

## Security Notes

- The default `recorder.service` runs as root for GPIO access
- For better security, use `recorder.service.txt` which runs as the `pi` user
- Ensure your `pi` user is in the `gpio` group: `sudo usermod -aG gpio pi`

## Dependencies

- Python 3
- RPi.GPIO
- evdev
- ffmpeg

## License

MIT License - feel free to use and modify for your own projects.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

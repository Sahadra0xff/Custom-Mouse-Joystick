# 🕹️ Custom Joystick Mouse — Arduino + Python

> A custom Human-Computer Interface that turns an analog joystick into a fully functional mouse controller.  
> Built with **Arduino Uno** + **Python** as part of a UEC project at LNMIIT.

**Authors:** Nitish Matta (24UEC217) & Jash Chirag Monani (24UEC206)  
**Institution:** LNMIIT, Jaipur

---

## 📸 Demo

The joystick's X/Y axes control cursor movement, and the built-in push-button acts as a left click. A non-linear acceleration curve allows both precise fine movements and fast screen traversal.

---

## 🏗️ System Architecture

```
[Analog Joystick] ──► [Arduino Uno] ──USB Serial──► [Python Script] ──► [OS Mouse Cursor]
```

| Component | Role |
|---|---|
| Analog Joystick | Reads X/Y axis + button |
| Arduino Uno (ATmega328P) | ADC reading, deadzone, acceleration, serial TX |
| Python (`mouse.py`) | Parses serial data, drives OS cursor via `pyautogui` |

---

## 🔌 Hardware Wiring

| Joystick Pin | Arduino Pin |
|---|---|
| GND | GND |
| +5V | 5V |
| VRx (X-axis) | A0 |
| VRy (Y-axis) | A1 |
| SW (Button) | D8 |

---

## 🚀 Getting Started

### 1. Upload Arduino Firmware

1. Open `Arduino_uno_mouse.ino` in the [Arduino IDE](https://www.arduino.cc/en/software).
2. Go to **Tools → Board** → Select **Arduino Uno**.
3. Go to **Tools → Port** → Select your COM port (e.g., `COM3`).
4. Click **Upload** (→ arrow button).

### 2. Install Python Dependencies

```bash
pip install pyserial pyautogui
```

### 3. Configure the COM Port

Open `mouse.py` and update this line to match your Arduino's port:

```python
COM_PORT = "COM3"      # Windows
# COM_PORT = "/dev/ttyACM0"   # Linux
# COM_PORT = "/dev/cu.usbmodem14101"  # macOS
```

### 4. Run the Script

```bash
python mouse.py
```

Move the joystick → cursor moves.  
Press the joystick button → left click.  
Press **Ctrl+C** in the terminal to stop.

---

## ⚙️ How It Works

### Deadzone
A central threshold (default: `±20` ADC units) ignores minor joystick imperfections so the cursor doesn't drift at rest.

### Acceleration Curve
Raw joystick input is normalized and then **squared** to create a non-linear response:
- Small deflections → slow, precise movement
- Large deflections → fast traversal

### Serial Protocol
```
<click_status> <deltaX> <deltaY> m
```
Example: `z 5 -3 m` (no click, move right 5px, up 3px)

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| Cursor doesn't move | Check COM port in `mouse.py`; verify Arduino TX light blinks |
| Cursor drifts at rest | Increase `DEADZONE` value in `.ino` file (try 25–30) |
| Movement only on one axis | Check VRx/VRy wiring; use Serial Monitor to verify both axes |
| Click doesn't work | Verify SW pin → D8; check Serial Monitor for `c` vs `z` |
| Movement is inverted | Negate `dx` or `dy` in `mouse.py` |

---

## 📈 SWOT Summary

| | |
|---|---|
| ✅ **Strengths** | Low cost, highly customizable, open-source, great educational value |
| ⚠️ **Weaknesses** | Lower precision than optical mouse, wired, no scroll wheel |
| 🌱 **Opportunities** | Bluetooth/Wi-Fi upgrade, scroll encoder, 3D-printed enclosure |
| ⚡ **Threats** | Library updates, OS permission issues, hardware wear |

---

## 🔮 Future Improvements

- [ ] Wireless via HC-05 Bluetooth or ESP32 Wi-Fi
- [ ] Rotary encoder for scroll wheel
- [ ] Right-click button support
- [ ] 3D-printed ergonomic enclosure
- [ ] Replace Python script with a proper USB HID driver

---

## 📚 References

- [Arduino Language Reference](https://www.arduino.cc/reference/en/)
- [pyserial Documentation](https://pyserial.readthedocs.io/)
- [pyautogui Documentation](https://pyautogui.readthedocs.io/)
- Margolis, M. (2012). *Make an Arduino-Controlled Robot*. O'Reilly Media.

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

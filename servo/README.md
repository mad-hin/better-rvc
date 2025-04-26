# Servo Setup

## Hardware List (in this section)

- Raspberry Pi 3B+
- MG90S Servo

## Connecting the Servo

![PI 3B+ GPIO Pinout](https://www.researchgate.net/publication/346085998/figure/fig2/AS:1003233170444288@1616200835027/Raspberry-Pi-3-B-Pin-out-Diagram-From-Fig-3-out-of-40-pins-26-are-used-as-a-digital.png)

Connect the servo to the Raspberry Pi GPIO pins as follows:

- **Power**: Connect the red wire of the servo to the 5V pin on the Raspberry Pi.
- **Ground**: Connect the brown wire of the servo to a ground pin on the Raspberry Pi.
- **Signal**: Connect the yellow wire of the servo to GPIO pin 7 on the Raspberry Pi (Refer to the above image).

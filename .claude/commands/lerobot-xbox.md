Lance le controle de X le Robot (2 bras) avec la manette Xbox.

Etapes :
1. Verifie que la manette Xbox est connectee : `cat /proc/bus/input/devices | grep -A 4 -i xbox`
2. Verifie les ports serie disponibles : `ls /dev/ttyACM*`
3. Lance le script :
```bash
cd ~/lerobot_pi/lerobot && source ../venv/bin/activate && python3 ~/lerobot_pi/xbox_control.py
```

Rappels :
- LB : changer de bras (bras 1 gauche 6 moteurs / bras 2 droit 4 moteurs)
- Stick G = shoulder_pan/lift, stick D = wrist_roll/flex, LT/RT = gripper, D-pad = elbow
- B = quitter
- La manette met du temps a se synchroniser, se deconnecte si inactive
- SPEED = 1.0, boucle 30Hz, auto-reconnect
- Ports : ACM0 = bras 1 (gauche), ACM1 = bras 2 (droit)

Si la manette n'est pas detectee, propose de verifier le Xbox 360 Wireless Receiver.

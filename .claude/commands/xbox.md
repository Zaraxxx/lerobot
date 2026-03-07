Lance le controle de X le Robot avec la manette Xbox.

Etapes :
1. Verifie que la manette Xbox est connectee : `cat /proc/bus/input/devices | grep -A 4 -i xbox`
2. Verifie le port serie disponible
3. Lance le script :
```bash
cd ~/lerobot_pi/lerobot && source ../venv/bin/activate && python3 ~/lerobot_pi/xbox_control.py
```

Rappels :
- La manette met du temps a se synchroniser
- Elle se deconnecte si inactive
- Mapping : stick G = shoulder_pan/lift, stick D = wrist_roll/flex, LT/RT = gripper, D-pad = elbow
- SPEED = 1.0, boucle 30Hz, auto-reconnect

Si la manette n'est pas detectee, propose de verifier le Xbox 360 Wireless Receiver.

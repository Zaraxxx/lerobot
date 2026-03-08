---
name: lerobot-xbox
description: Controle du robot via manette Xbox
user-invocable: true
---

# Controle Manette Xbox

Lance le script de controle du robot via la manette Xbox.

## Etapes

1. Verifier que la manette est connectee : `cat /proc/bus/input/devices | grep -A 4 -i xbox`
2. Verifier les ports serie : `ls /dev/ttyACM* 2>/dev/null`
3. Lancer le script : `cd ~/lerobot_pi/lerobot && source ../venv/bin/activate && python3 ~/lerobot_pi/xbox_control.py`

## Mapping actuel
- Stick gauche : shoulder_pan (X) / shoulder_lift (Y)
- Stick droit : wrist_roll (X) / wrist_flex (Y)
- LT/RT : gripper (ouvrir/fermer)
- D-pad haut/bas : elbow_flex
- LB : switcher entre bras gauche et droit
- B : quitter

## Notes
- La manette met du temps a se synchroniser
- Se deconnecte si inactive trop longtemps
- Le script gere l'auto-reconnexion
- SPEED = 1.0, boucle 30Hz

---
name: lerobot-status
description: Diagnostic systeme complet du robot
user-invocable: true
---

# Diagnostic Systeme LeRobot

Execute un diagnostic complet du systeme. Lance les commandes suivantes et presente un rapport clair :

## Verifications a effectuer

1. **Ports serie** : `ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null` - Lister les ports disponibles
2. **Manette Xbox** : `cat /proc/bus/input/devices | grep -A 4 -i xbox` - Verifier si la manette est detectee
3. **Cameras** : `v4l2-ctl --list-devices 2>/dev/null` - Lister les cameras
4. **Espace disque** : `df -h /` - Verifier l'espace disponible sur le SSD NVMe
5. **Python/venv** : Verifier que le venv est actif et les packages installes
6. **Processus** : `ps aux | grep -E "python|lerobot" | grep -v grep` - Verifier les processus en cours

## Format du rapport

Presente les resultats sous forme de liste avec des indicateurs OK/ERREUR pour chaque verification.

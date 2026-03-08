---
name: lerobot-record
description: Enregistrement de donnees (dataset)
user-invocable: true
---

# Enregistrement de Donnees LeRobot

Lance l'enregistrement d'episodes pour creer un dataset.

## Etapes

1. Verifier les ports serie : `ls /dev/ttyACM* 2>/dev/null`
2. Verifier les cameras : `v4l2-ctl --list-devices 2>/dev/null`
3. Identifier le fichier de config dans `config/record/` :
   - `zarax_record_config_pi.yaml` pour Raspberry Pi 5
   - `zarax_record_config_camdroite.yaml` pour Windows 1 camera
4. Activer le venv : `source ~/lerobot_pi/venv/bin/activate`
5. Lancer l'enregistrement avec la config appropriee

## Dataset existant
- `Zarax/zarax-demo` : 9 episodes, 3491 frames

## Notes
- S'assurer que leader ET follower sont branches
- Les cameras doivent etre detectees avant de lancer
- Chaque episode est sauvegarde automatiquement

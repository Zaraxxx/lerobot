---
name: lerobot-teleop
description: Teleoperation leader/follower
user-invocable: true
---

# Teleoperation LeRobot

Lance la teleoperation leader/follower.

## Etapes

1. Verifier les ports serie : `ls /dev/ttyACM* 2>/dev/null`
2. Identifier le fichier de config adapte dans `config/teleop/` :
   - `zarax_teleop_config_pi.yaml` pour Raspberry Pi 5
   - `zarax_teleop_config_camdroite.yaml` pour Windows 1 camera
   - `zarax_teleop_config_2cam.yaml` pour Windows 2 cameras
3. Activer le venv : `source ~/lerobot_pi/venv/bin/activate`
4. Lancer la teleoperation avec la config appropriee

## Notes
- Verifier que les deux bras sont branches (leader + follower)
- Les ports serie changent au rebranchement
- Calibration necessaire si c'est la premiere utilisation

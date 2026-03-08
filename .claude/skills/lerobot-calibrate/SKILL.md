---
name: lerobot-calibrate
description: Calibration des moteurs du robot
user-invocable: true
---

# Calibration Moteurs LeRobot

Lance la calibration des moteurs du robot.

## Etapes

1. Verifier les ports serie : `ls /dev/ttyACM* 2>/dev/null`
2. Activer le venv : `source ~/lerobot_pi/venv/bin/activate`
3. Lancer la calibration pour le bras souhaite

## Fichiers de calibration existants
- Follower : `~/.cache/huggingface/lerobot/calibration/robots/so_follower/zarax.json`
- Leader : `~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/zarax.json`

## Notes
- Les positions sont normalisees de -100 a +100
- Moteurs STS3215 (model 777), Feetech
- 6 moteurs par bras (ID 1-6)
- Demander a l'utilisateur quel bras calibrer (follower/leader, gauche/droit)

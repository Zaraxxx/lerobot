Lance la calibration des moteurs de X le Robot.

Etapes :
1. Demande a l'utilisateur quel bras calibrer :
   - **follower** (robot) : sauvegarde dans `~/.cache/huggingface/lerobot/calibration/robots/so_follower/zarax.json`
   - **leader** (teleoperateur) : sauvegarde dans `~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/zarax.json`
2. Verifie le port serie disponible
3. Lance la calibration :
```bash
cd ~/lerobot_pi/lerobot && source ../venv/bin/activate && python -m lerobot.calibrate --robot.type=so100_follower --robot.port=/dev/ttyACM0 --robot.id=zarax
```
   Ou pour le leader :
```bash
python -m lerobot.calibrate --teleop.type=so100_leader --teleop.port=/dev/ttyACM0 --teleop.id=zarax
```

4. Apres la calibration, verifie que le fichier JSON a ete cree/mis a jour.

Notes :
- Moteurs STS3215 (model 777), Feetech
- Positions normalisees de -100 a +100

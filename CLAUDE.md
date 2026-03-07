# X le Robot - Configuration et Progression

## Contexte
"X le robot" - Robot avec deux bras (leader et follower) utilisant LeRobot (Hugging Face) pour la teleoperation et la collecte de donnees.

---

## Statut actuel - 2026-03-07 (SESSION 5)

### Ce qui est fait
1. **Montage du robot** : Assemblage complet
2. **Configuration des bras** :
   - Bras 1 : 4 moteurs (ID 1-4), 2 moteurs manquants (5, 6)
   - Bras 2 : 6 moteurs (ID 1-6), complet et fonctionnel
   - Calibration sauvegardee : `~/.cache/huggingface/lerobot/calibration/robots/so_follower/zarax.json`
   - Calibration leader : `~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/zarax.json`
3. **RPi5 operationnel** :
   - PyTorch 2.10.0 (CPU), OpenCV 4.12.0, LeRobot 0.4.4
   - Python 3.13, venv : `~/lerobot_pi/venv/`
   - Claude Code installe
4. **Manette Xbox** :
   - Xbox 360 Wireless Receiver sur `/dev/input/event5` et `/dev/input/js0`
   - Script de controle : `~/lerobot_pi/xbox_control.py`
   - Teste et fonctionnel avec le bras 2 (6 moteurs)
   - Mapping : stick G = shoulder_pan/lift, stick D = wrist_roll/flex, LT/RT = gripper, D-pad = elbow
   - SPEED = 1.0, boucle 30Hz, auto-reconnect
   - NOTE : la manette met du temps a se synchroniser, se deconnecte si inactive
5. **Collecte de donnees (Windows)** :
   - Dataset : `Zarax/zarax-demo` (9 episodes, 3,491 frames)
6. **Modele ACT (Windows)** :
   - Entraine sur 20,000 steps, loss 0.035
   - Uploade : `Zarax/act-zarax-v1`

### A faire
- Changer le mapping de la manette Xbox (a definir)
- Ajouter le controle du deuxieme bras (4 moteurs)
- Reduire la vitesse si necessaire

### Environnement Raspberry Pi
- **OS** : Linux Debian aarch64, Kernel 6.12.47
- **Hostname** : PiRobot
- **User** : zarax
- **Repo** : `~/lerobot_pi/lerobot/` (clone de https://github.com/Zaraxxx/lerobot)
- **Venv** : `source ~/lerobot_pi/venv/bin/activate`
- **Ports serie** : `/dev/ttyACM0` (change selon branchement)
- **Moteurs** : STS3215 (model 777), Feetech

### Environnement Windows (PC principal)
- Windows 11, Python 3.10 (conda: lerobot)
- SSH vers Pi : `ssh -i ~/.ssh/id_ed25519_pi zarax@192.168.1.78`
- Acces SSH uniquement depuis le PC Flav-Laptop

---

## API LeRobot (reference rapide)

```python
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors.motors_bus import Motor, MotorCalibration, MotorNormMode

# Creer un bus moteur
motors = {"shoulder_pan": Motor(1, "sts3215", MotorNormMode.RANGE_M100_100)}
calibration = {"shoulder_pan": MotorCalibration(id=1, drive_mode=0, homing_offset=272, range_min=861, range_max=3364)}
bus = FeetechMotorsBus(port="/dev/ttyACM0", motors=motors, calibration=calibration)
bus.connect()

# Lire/ecrire
pos = bus.read("Present_Position", "shoulder_pan")
bus.write("Goal_Position", "shoulder_pan", 50.0)  # write(registre, nom_moteur, valeur)
bus.disconnect()
```

---

## Scripts utiles

### Controle manette Xbox
```bash
cd ~/lerobot_pi/lerobot && source ../venv/bin/activate
python3 ~/lerobot_pi/xbox_control.py
```

### Diagnostic
```bash
# Ports serie
ls /dev/ttyACM* /dev/ttyUSB*

# Manette
cat /proc/bus/input/devices | grep -A 4 xbox

# Cameras
v4l2-ctl --list-devices
```

---

## Fichiers de configuration

```
config/
  teleop/
    zarax_teleop_config_pi.yaml          # Raspberry Pi 5
    zarax_teleop_config_camdroite.yaml   # Windows, 1 camera
    zarax_teleop_config_2cam.yaml        # Windows, 2 cameras
  record/
    zarax_record_config_pi.yaml          # Raspberry Pi 5
    zarax_record_config_camdroite.yaml   # Windows, 1 camera
  eval/
    zarax_eval_simple.yaml               # Evaluation avec modele ACT
```

---

## Notes techniques

- **write() API** : `bus.write("Goal_Position", motor_name, value)` - nom du moteur AVANT la valeur
- **Manette Xbox** : utiliser evdev, la manette se deconnecte souvent, toujours gerer la reconnexion
- **Ports serie Linux** : `/dev/ttyACM0`, les numeros changent au rebranchement
- **Calibration** : positions normalisees de -100 a +100

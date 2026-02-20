# X le Robot - Configuration et Progression

## Contexte
"X le robot" - Robot avec deux bras (leader et follower) utilisant LeRobot (Hugging Face) pour la teleoperation et la collecte de donnees.

---

## Statut actuel - 2026-02-20 (SESSION 4)

### Ce qui est fait
1. **Montage du robot** : Assemblage complet
2. **Configuration des bras** :
   - Bras leader : calibre (COM8)
   - Bras follower : calibre (COM7) avec ID "zarax"
   - Calibration sauvegardee : `~/.cache/huggingface/lerobot/calibration/robots/so_follower/zarax.json`
3. **Synchronisation** : Les deux bras fonctionnent en mode miroir
4. **Cameras** :
   - Configurees : USB indice 1 (640x480, 30 FPS)
   - Testees et fonctionnelles avec OpenCV
5. **Teleoperation complete** :
   - Bras leader et follower synchronises
   - Flux video camera affiches en temps reel
   - Visualisation Rerun activee (`display_data: true`)
   - Pas de deconnexions lors du test
6. **Collecte de donnees** :
   - Dataset enregistre : `Zarax/zarax-demo` (9 episodes, 3,491 frames)
   - Fichier de config : `config/record/zarax_record_config_camdroite.yaml`
7. **Entrainement du modele** :
   - Modele ACT entraine sur 20,000 steps
   - Loss finale : 0.035
   - Modele uploade : `Zarax/act-zarax-v1`
   - Checkpoint local : `outputs/train/act_zarax_v1/checkpoints/020000/`
8. **Deploiement** :
   - Robot fonctionne en mode autonome avec le modele entraine
   - Script simple : `run_model.bat`
   - Config : `config/eval/zarax_eval_simple.yaml`
9. **Setup RPi5** : En cours
   - Configs Pi creees, script d'installation pret
   - Voir `plans/rpi5_setup.md`

### Environnement
- **Windows** : Windows 10/11, Python 3.10 (conda: `lerobot`), LeRobot main (post-v0.4.4)
- **Raspberry Pi 5** : Setup en cours (voir `plans/rpi5_setup.md`)
- Cameras USB : indice 1 (640x480, 30 FPS)
- Robot ID : "zarax"

---

## Progression

| Etape | Statut | Description |
|-------|--------|-------------|
| 1. Montage | Complete | Robot assemble et operationnel |
| 2. Calibration | Complete | Bras calibres (zarax.json) |
| 3. Teleoperation | Complete | Leader/Follower synchronises avec cameras |
| 4. Collecte de donnees | Complete | 9 episodes enregistres (Zarax/zarax-demo) |
| 5. Entrainement | Complete | Modele ACT entraine (Zarax/act-zarax-v1) |
| 6. Deploiement | Complete | Robot fonctionne en mode autonome |
| 7. Setup RPi5 | En cours | Installer LeRobot sur Raspberry Pi 5 |

---

## Fichiers de configuration

### Structure des configs
```
config/
  teleop/
    zarax_teleop_config_2cam.yaml       # Windows, 2 cameras
    zarax_teleop_config_camdroite.yaml   # Windows, 1 camera (principal)
    zarax_teleop_config_nocam.yaml       # Windows, sans cameras
    zarax_teleop_config_pi.yaml          # Raspberry Pi 5
    zarax_teleop_config_EXAMPLE.yaml     # Reference complete commentee
  record/
    zarax_record_config_camdroite.yaml   # Windows, 1 camera
    zarax_record_config_pi.yaml          # Raspberry Pi 5
    zarax_record_config_EXAMPLE.yaml     # Reference complete commentee
  eval/
    zarax_eval_simple.yaml               # Evaluation avec modele ACT
```

---

## Commandes utiles

### Environnement
```bash
# Windows (conda)
conda activate lerobot
cd C:\XLeRobot\lerobot

# Raspberry Pi (venv)
cd ~/lerobot_pi/lerobot && source ../venv/bin/activate
```

### Diagnostic
```bash
lerobot-find-cameras opencv
lerobot-find-port
```

### Teleoperation
```bash
# Windows - 1 camera
lerobot-teleoperate --config_path config/teleop/zarax_teleop_config_camdroite.yaml

# Raspberry Pi
lerobot-teleoperate --config_path config/teleop/zarax_teleop_config_pi.yaml
```

### Collecte de donnees
```bash
lerobot-record --config_path config/record/zarax_record_config_camdroite.yaml
```

### Deploiement modele
```bash
.\run_model.bat
```

---

## Notes techniques

- **Backend OpenCV Windows** : Utiliser `backend: DSHOW` dans le YAML (DirectShow). Depuis la derniere mise a jour upstream, le backend est configurable par camera dans le YAML (plus de modification de `utils.py`)
- **Backend OpenCV Linux/Pi** : `backend: ANY` (defaut, pas besoin de le specifier)
- **Cv2Backends disponibles** : ANY, V4L2, DSHOW, PVAPI, ANDROID, AVFOUNDATION, MSMF (voir `src/lerobot/cameras/configs.py`)
- **Calibration** : Sauvegardee automatiquement dans zarax.json
- **Cameras** : OpenCV camera config accepte `index_or_path` (entier ou chemin vers fichier video)
- **Format CLI** : Utiliser `--config_path` (underscore) et non `--config-path` (tiret)
- **Deploiement** : LeRobot n'a pas de mode "inference-only" natif, il faut `num_episodes >= 1`

---

## Plans et documentation

- `plans/rpi5_setup.md` - Plan d'installation sur Raspberry Pi 5
- `scripts/setup_pi.sh` - Script d'installation automatise pour RPi5

---

## Ressources

- [LeRobot Documentation](https://huggingface.co/docs/lerobot)
- [Tutorial complet](https://huggingface.co/docs/lerobot/tutorials)
- [Teleoperation guide](https://huggingface.co/docs/lerobot/teleop)
- [Dataset guide](https://huggingface.co/docs/lerobot/datasets)

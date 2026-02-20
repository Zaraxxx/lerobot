# Plan : Installation LeRobot sur Raspberry Pi 5

## Contexte

Le projet "X le Robot" (zarax) fonctionne sur Windows avec 2 bras SO101 et 2 cameras USB. L'objectif est d'installer la meme config sur un Raspberry Pi 5 pour la **teleoperation et collecte de donnees** (entrainement sur PC Windows). Les deux setups coexisteront.

**Methode de deploiement :** SSH depuis le PC Windows une fois le Pi configure.

---

## Phase A : Preparer le repo GitHub (sur le PC Windows)

### A1. Nettoyer et organiser les fichiers

**Fichiers commites** (audit de securite : tous safe, aucune donnee sensible) :
- `config/teleop/*.yaml` - configs teleoperation (Windows + Pi)
- `config/record/*.yaml` - configs collecte de donnees (Windows + Pi)
- `plans/rpi5_setup.md` - ce plan de deploiement (accessible depuis tout PC)
- `.claude/` - config et memoire Claude Code (synchronise entre PCs)
- `CLAUDE.md` - documentation projet
- `delete_datasets.py` + `delete_datasets.bat` - utilitaires
- `FDTEST.py` - script de test
- `src/lerobot/cameras/utils.py` - modification CAP_DSHOW (deja faite)
- `scripts/setup_pi.sh` - script d'installation automatise pour RPi5

### A2. Configs RPi5 (YAML Linux)

**`config/teleop/zarax_teleop_config_pi.yaml`** - Teleoperation sur Pi
**`config/record/zarax_record_config_pi.yaml`** - Collecte de donnees sur Pi

Les ports `/dev/ttyUSB*` et `/dev/video*` doivent etre adaptes selon la detection sur le Pi.

---

## Phase B : Preparer le Raspberry Pi 5 (manuel par l'utilisateur)

### B1. Materiel requis
- RPi5 (8GB recommande) + carte SD 64GB+ + alimentation 27W
- **Refroidissement actif** (obligatoire pour teleoperation continue)
- 4 ports USB : 2 adaptateurs serie (bras) + 2 cameras

### B2. Flasher l'OS

Avec **Raspberry Pi Imager** sur le PC Windows :
- OS : **Raspberry Pi OS 64-bit (Bookworm) avec desktop**
- Settings : activer SSH, configurer username/password, configurer WiFi
- Desktop necessaire pour la visualisation Rerun (`display_data: true`)

### B3. Premier demarrage et IP

```bash
# Sur le Pi ou via SSH initial
sudo apt update && sudo apt full-upgrade -y
hostname -I   # Noter l'adresse IP pour le deploiement SSH
```

> **Le user communique l'IP du Pi** pour que je puisse deployer via SSH.

---

## Phase C : Deploiement via SSH (depuis le PC Windows)

### C1. Option automatique : script setup

```bash
# Copier le script sur le Pi
scp scripts/setup_pi.sh pi@<IP>:~/setup_pi.sh
# Executer
ssh pi@<IP> "chmod +x ~/setup_pi.sh && ~/setup_pi.sh"
```

### C2. Option manuelle : etapes individuelles

#### Installer les dependances systeme

```bash
ssh pi@<IP> "sudo apt install -y build-essential cmake git curl wget \
  python3-dev python3-pip python3-venv \
  ffmpeg libavcodec-dev libavformat-dev libavutil-dev libswscale-dev libswresample-dev libavfilter-dev \
  libopencv-dev python3-opencv libv4l-dev v4l-utils \
  libusb-1.0-0-dev speech-dispatcher espeak-ng \
  libhdf5-dev libjpeg-dev libpng-dev libtiff-dev"
```

#### Configurer les permissions

```bash
ssh pi@<IP> "sudo usermod -a -G dialout,video,input \$USER"
ssh pi@<IP> "sudo reboot"
```

#### Installer LeRobot

```bash
ssh pi@<IP> << 'EOF'
mkdir -p ~/lerobot_pi && cd ~/lerobot_pi
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
git clone https://github.com/huggingface/lerobot.git
cd lerobot
git checkout v0.4.4
pip install -e ".[feetech]"
EOF
```

> **Pourquoi `[feetech]` et non `[pi]` ?** `[pi]` = politiques Pi0/Pi0.5 (inference IA). `[feetech]` = moteurs STS3215 du SO101, suffisant pour teleop + collecte.

#### Transferer la calibration

```bash
# Depuis le PC Windows
scp ~/.cache/huggingface/lerobot/calibration/robots/so_follower/zarax.json \
    pi@<IP>:~/.cache/huggingface/lerobot/calibration/robots/so_follower/zarax.json

scp ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/zarax.json \
    pi@<IP>:~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/zarax.json
```

#### Optimiser la carte SD

```bash
ssh pi@<IP> << 'EOF'
echo "tmpfs /tmp tmpfs defaults,noatime,size=512M 0 0" | sudo tee -a /etc/fstab
sudo dphys-swapfile swapoff
sudo sed -i 's/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=100/' /etc/dphys-swapfile
sudo dphys-swapfile setup && sudo dphys-swapfile swapon
EOF
```

#### Verification

```bash
ssh pi@<IP> << 'EOF'
cd ~/lerobot_pi/lerobot && source ../venv/bin/activate
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import cv2; print(f'OpenCV: {cv2.__version__}')"
python -c "import lerobot; print(f'LeRobot: {lerobot.__version__}')"
lerobot-find-port --help
lerobot-find-cameras --help
EOF
```

---

## Phase D : Configuration des peripheriques (interactif via SSH)

Cette phase necessite que les bras et cameras soient branches au Pi.

### D1. Identifier les ports serie

```bash
ssh pi@<IP> "ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null"
```

### D2. Identifier les cameras

```bash
ssh pi@<IP> "v4l2-ctl --list-devices"
```

### D3. Adapter les configs YAML

Mettre a jour les fichiers YAML avec les vrais chemins trouves en D1/D2.

### D4. Test teleoperation

```bash
ssh pi@<IP> "cd ~/lerobot_pi/lerobot && source ../venv/bin/activate && \
  lerobot-teleoperate --config_path config/teleop/zarax_teleop_config_pi.yaml"
```

### D5. Test collecte de donnees (1 episode)

```bash
ssh pi@<IP> "cd ~/lerobot_pi/lerobot && source ../venv/bin/activate && \
  lerobot-record --config_path config/record/zarax_record_config_pi.yaml \
  --dataset.repo_id zarax/test-pi --dataset.num_episodes 1 --dataset.push_to_hub false"
```

---

## Resume

| Phase | Qui | Quoi |
|-------|-----|------|
| **A** | Claude (PC Windows) | Committer configs + script setup dans GitHub |
| **B** | Utilisateur | Flasher RPi5 OS, activer SSH, communiquer l'IP |
| **C** | Claude (SSH) | Installer dependances, LeRobot, transferer calibration |
| **D** | Claude (SSH) | Configurer peripheriques USB, tester teleop + collecte |

## Aucune modification du code source necessaire

Tout est gere par la detection de plateforme existante dans LeRobot et les fichiers YAML specifiques Linux.

## Fichiers cles references

- `src/lerobot/cameras/utils.py` - Backend OpenCV (multi-plateforme, CAP_ANY sur Linux)
- `src/lerobot/cameras/opencv/camera_opencv.py:302` - Detection cameras Linux /dev/video*
- `src/lerobot/scripts/lerobot_find_port.py:37` - Detection ports serie Linux /dev/tty*
- `src/lerobot/utils/constants.py:71` - Chemin calibration
- `config/teleop/zarax_teleop_config_2cam.yaml` - Config Windows (reference)

## Problemes potentiels et solutions

| Probleme | Solution |
|----------|----------|
| `rerun-sdk` ne s'installe pas sur ARM64 | Mettre `display_data: false` |
| PyTorch compile depuis les sources (lent) | Verifier les wheels ARM64 pre-compiles |
| Temperature > 80C pendant teleop | Refroidissement actif + reduire a 1 camera |
| Codec video AV1 trop lent sur ARM | Utiliser `--dataset.video_codec=h264` |
| Ports USB changent au reboot | Creer regles udev (etape optionnelle) |

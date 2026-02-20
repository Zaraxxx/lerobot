#!/usr/bin/env bash
# ========================================================================
# Script d'installation LeRobot sur Raspberry Pi 5
# ========================================================================
# Usage:
#   chmod +x scripts/setup_pi.sh
#   ./scripts/setup_pi.sh
#
# Ce script installe toutes les dependances et LeRobot v0.4.4
# sur un Raspberry Pi 5 avec Raspberry Pi OS 64-bit (Bookworm).
# ========================================================================

set -euo pipefail

LEROBOT_VERSION="v0.4.4"
INSTALL_DIR="$HOME/lerobot_pi"

echo "============================================"
echo " Installation LeRobot $LEROBOT_VERSION sur RPi5"
echo "============================================"

# ---- Etape 1 : Mise a jour systeme ----
echo ""
echo "[1/7] Mise a jour du systeme..."
sudo apt update && sudo apt full-upgrade -y

# ---- Etape 2 : Dependances systeme ----
echo ""
echo "[2/7] Installation des dependances systeme..."
sudo apt install -y \
  build-essential cmake git curl wget \
  python3-dev python3-pip python3-venv \
  ffmpeg libavcodec-dev libavformat-dev libavutil-dev \
  libswscale-dev libswresample-dev libavfilter-dev \
  libopencv-dev python3-opencv libv4l-dev v4l-utils \
  libusb-1.0-0-dev speech-dispatcher espeak-ng \
  libhdf5-dev libjpeg-dev libpng-dev libtiff-dev

# ---- Etape 3 : Permissions utilisateur ----
echo ""
echo "[3/7] Configuration des permissions (dialout, video, input)..."
sudo usermod -a -G dialout,video,input "$USER"

# ---- Etape 4 : Environnement Python ----
echo ""
echo "[4/7] Creation de l'environnement Python..."
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip setuptools wheel

# ---- Etape 5 : Installation LeRobot ----
echo ""
echo "[5/7] Clonage et installation de LeRobot..."
if [ ! -d "lerobot" ]; then
  git clone https://github.com/huggingface/lerobot.git
fi
cd lerobot
git checkout "$LEROBOT_VERSION"
pip install -e ".[feetech]"

# ---- Etape 6 : Optimisation carte SD ----
echo ""
echo "[6/7] Optimisation de la carte SD..."
# Tmpfs en RAM pour reduire l'usure
if ! grep -q "tmpfs /tmp" /etc/fstab; then
  echo "tmpfs /tmp tmpfs defaults,noatime,size=512M 0 0" | sudo tee -a /etc/fstab
  echo "  -> tmpfs /tmp ajoute"
else
  echo "  -> tmpfs /tmp deja configure"
fi

# Reduire le swap
if [ -f /etc/dphys-swapfile ]; then
  sudo dphys-swapfile swapoff
  sudo sed -i 's/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=100/' /etc/dphys-swapfile
  sudo dphys-swapfile setup
  sudo dphys-swapfile swapon
  echo "  -> Swap reduit a 100 MB"
fi

# ---- Etape 7 : Verification ----
echo ""
echo "[7/7] Verification de l'installation..."
echo ""
python -c "import torch; print(f'  PyTorch: {torch.__version__}')"
python -c "import cv2; print(f'  OpenCV:  {cv2.__version__}')"
python -c "import lerobot; print(f'  LeRobot: {lerobot.__version__}')"
echo ""

# Verification des commandes CLI
if command -v lerobot-find-port &> /dev/null; then
  echo "  lerobot-find-port:    OK"
else
  echo "  lerobot-find-port:    NON TROUVE (verifier PATH)"
fi

if command -v lerobot-find-cameras &> /dev/null; then
  echo "  lerobot-find-cameras: OK"
else
  echo "  lerobot-find-cameras: NON TROUVE (verifier PATH)"
fi

echo ""
echo "============================================"
echo " Installation terminee!"
echo "============================================"
echo ""
echo "IMPORTANT: Redemarrez le Pi pour appliquer les permissions:"
echo "  sudo reboot"
echo ""
echo "Apres redemarrage, activez l'environnement avec:"
echo "  cd $INSTALL_DIR/lerobot && source ../venv/bin/activate"
echo ""
echo "Puis testez avec:"
echo "  lerobot-find-port"
echo "  lerobot-find-cameras opencv"
echo ""

Effectue un diagnostic complet du systeme X le Robot sur le Raspberry Pi.

Verifie les elements suivants et affiche un rapport clair :

1. **Ports serie** : `ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null` - verifier quels ports sont disponibles
2. **Manette Xbox** : `cat /proc/bus/input/devices | grep -A 4 -i xbox` - verifier si la manette est connectee
3. **Cameras** : `v4l2-ctl --list-devices 2>/dev/null` - lister les cameras disponibles
4. **Processus robot** : `ps aux | grep -E "lerobot|xbox_control" | grep -v grep` - verifier si un processus robot tourne
5. **Espace disque** : `df -h /` - verifier l'espace disponible
6. **Etat du venv** : verifier que `~/lerobot_pi/venv/` existe

Affiche un resume clair avec le statut de chaque element (OK / NON TROUVE / ERREUR).

---
name: lerobot-cameras
description: Verification des cameras connectees
user-invocable: true
---

# Verification Cameras LeRobot

Verifie les cameras connectees au systeme.

## Etapes

1. Lister les peripheriques video : `v4l2-ctl --list-devices 2>/dev/null`
2. Lister les fichiers video : `ls /dev/video* 2>/dev/null`
3. Pour chaque camera detectee, afficher les formats supportes : `v4l2-ctl --device=/dev/videoX --list-formats-ext 2>/dev/null`

## Format du rapport
Presenter un resume clair :
- Nombre de cameras detectees
- Nom et chemin de chaque camera
- Resolutions supportees

## Notes
- Les cameras USB peuvent changer de numero au rebranchement
- Verifier que les cameras ne sont pas utilisees par un autre processus

Lance la teleoperation de X le Robot sur le Raspberry Pi.

Etapes :
1. Verifie que le port serie est disponible (`/dev/ttyACM0` ou autre)
2. Verifie quelle config utiliser parmi :
   - `config/teleop/zarax_teleop_config_pi.yaml` (avec cameras)
   - `config/teleop/zarax_teleop_config_pi_1cam.yaml` (1 camera)
   - `config/teleop/zarax_teleop_config_pi_nocam.yaml` (sans camera)
3. Demande a l'utilisateur quelle config utiliser si pas clair
4. Lance la commande :
```bash
cd ~/lerobot_pi/lerobot && source ../venv/bin/activate && python -m lerobot.teleop --config <config_choisie>
```

Si une erreur survient, diagnostique et propose une solution.

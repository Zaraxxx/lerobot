Lance l'enregistrement de donnees (collecte d'episodes) pour X le Robot.

Etapes :
1. Verifie que le port serie est disponible
2. Verifie les cameras connectees
3. Utilise la config : `config/record/zarax_record_config_pi.yaml`
4. Demande a l'utilisateur le nom du dataset et le nombre d'episodes si pas specifie
5. Lance la commande :
```bash
cd ~/lerobot_pi/lerobot && source ../venv/bin/activate && python -m lerobot.record --config config/record/zarax_record_config_pi.yaml
```

Apres l'enregistrement, propose de push le dataset sur Hugging Face Hub.

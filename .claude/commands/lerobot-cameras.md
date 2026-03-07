Verifie les cameras connectees au Raspberry Pi pour X le Robot.

Etapes :
1. Liste les cameras : `v4l2-ctl --list-devices 2>/dev/null`
2. Verifie les devices video : `ls /dev/video* 2>/dev/null`
3. Pour chaque camera trouvee, affiche les formats supportes : `v4l2-ctl -d /dev/videoX --list-formats-ext 2>/dev/null`
4. Teste si OpenCV peut ouvrir les cameras avec un script Python rapide si necessaire

Affiche un resume clair : nombre de cameras, devices, resolutions disponibles.

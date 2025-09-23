# raspi-robot

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Lancement du programme la connexion de la manette xbox :
  * robot.rules => /etc/udev/rules.d
  * robot.service => /etc/systemd/system
  * robot.sh => /home/yann/raspi-robot
La règle (robot.rules) lance le service (robot.service) qui lance le script (robot.sh) qui lance le programme (robot.py)

commandes utiles :
sudo nano /etc/systemd/system/robot.service (modifier le fichier service)
sudo systemctl daemon-reload (relance les services)
sudo systemctl status robot (voir le status du service)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

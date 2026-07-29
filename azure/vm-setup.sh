#!/bin/bash
# cd ~ && mkdir dev && curl -fsSL https://raw.githubusercontent.com/EleazarAldayG/app-asistencia-con-fallas/refs/heads/main/azure/vm-setup.sh -o ~/dev/vm-setup.sh && sudo chmod +x ~/dev/vm-setup.sh && cd dev/ && sudo ./vm-setup.sh > ~/setup.log
sudo apt update

echo "Instalando stack..."

sudo apt install -y default-mysql-server python3 python3-pip python3-venv git

echo "Clonando proyecto de GitHub..."

cd ~/dev/ && git clone https://github.com/EleazarAldayG/app-asistencia-con-fallas.git && cd app-asistencia-con-fallas

echo "Proyecto clonado! Descargando requirements"

python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

echo "Creando servicios para inicio automatico"

sed -i "s/userdir/$USER/g" api-service-setup.ini
sudo cp api-service-setup.ini /etc/systemd/system/myapi.service
sudo systemctl daemon-reload
sudo systemctl enable mysql
sudo systemctl start mysql
sudo systemctl start myapi
sudo systemctl enable myapi

echo "Checking MySQL installation..."

sudo mysql < ./db-setup.sql 2>&1

echo "Database setup completed successfully."

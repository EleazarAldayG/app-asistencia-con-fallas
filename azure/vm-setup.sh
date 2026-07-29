#!/bin/bash
# sudo curl -fsSL https://raw.githubusercontent.com/EleazarAldayG/app-asistencia-con-fallas/refs/heads/main/azure/vm-setup.sh -o /home/dev/vm-setup.sh && chmod +x /home/dev/vm-setup.sh && chown tdp:tdp /home/dev/vm-setup.sh && sudo -u tdp bash /home/dev/vm-setup.sh > /home/dev/setup.log 2>&1
sudo apt update

echo "Instalando stack..."

sudo apt install default-mysql-server python3 python3-pip python3-venv git

echo "Clonando proyecto de GitHub..."

cd /home && sudo mkdir dev && cd dev && git clone https://github.com/EleazarAldayG/app-asistencia-con-fallas.git && cd app-asistencia-con-fallas

echo "Proyecto clonado! Descargando requirements"

python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

echo "Creando servicios para inicio automatico"

sudo cp api-service-setup.ini /etc/systemd/system/myapi.service
sudo systemctl daemon-reload
sudo systemctl enable mysql
sudo systemctl start mysql
sudo systemctl start myapi
sudo systemctl enable myapi

set -e

SQL_FILE="./home/dev/app-asistencia-con-fallas/db-setup.sql"

echo "Checking MySQL installation..."

echo "Executing SQL script: $SQL_FILE"
sudo mysql < "$SQL_FILE" 2>&1

echo "Database setup completed successfully."

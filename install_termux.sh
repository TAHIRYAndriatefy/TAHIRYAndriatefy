pkg update -y
pkg install python -y
pip install telethon rich

termux-open-url "https://my.telegram.org"

echo "Connecte-toi et clique sur 'API development tools' puis crée une application."
read -p "API ID: " api_id
read -p "API HASH: " api_hash
read -p "Téléphone (+XXX...): " phone

echo "{\"api_id\": $api_id, \"api_hash\": \"$api_hash\", \"phone\": \"$phone\"}" > config.json

echo "python bnb_collector.py" > bnbbot
chmod +x bnbbot
mv bnbbot /data/data/com.termux/files/usr/bin/

echo "bnbbot" >> ~/.bashrc

echo "[✓] Installation terminée. Le bot se lancera automatiquement à l'ouverture de Termux."

mv bnbbot-disable /data/data/com.termux/files/usr/bin/
mv bnbbot-enable /data/data/com.termux/files/usr/bin/
chmod +x /data/data/com.termux/files/usr/bin/bnbbot-disable
chmod +x /data/data/com.termux/files/usr/bin/bnbbot-enable

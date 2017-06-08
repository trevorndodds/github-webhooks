# github-webhooks


## protected-webhook

Create Systemd service

Create Folder and copy webhook:
```
sudo mkdir -p /data/scripts/webhooks/
sudo cp /tmp/protected-webhook.py /data/scripts/webhooks/
```
Create Service
```
sudo vi /etc/systemd/system/gh-protected-webhook.service
```
Copy the below in the service file:
```
[Unit]
Description=GitHub Potected-Webhook
After=multi-user.target

[Service]
Environment=PYTHONUNBUFFERED=true
Type=simple
ExecStart=/data/scripts/webhooks/protected-webhook.py
User=root
WorkingDirectory=/data/scripts/webhooks/
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Execute:
```
sudo chmod 664 /etc/systemd/system/gh-protected-webhook.service
sudo chmod +x /data/scripts/webhooks/protected-webhook.py
```
Register and Start the Service:
```
sudo systemctl enable gh-protected-webhook.service
sudo systemctl daemon-reload
sudo systemctl start gh-protected-webhook.service
```
To View Status and logs execute:
```
sudo systemctl status gh-protected-webhook.service -l
sudo journalctl -u gh-protected-webhook.service -xn -l
sudo journalctl -u gh-protected-webhook.service
```

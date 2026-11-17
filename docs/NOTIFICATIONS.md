# Alert notifications

The `alert-notifier` service watches the Wazuh manager's shared `alerts.json` log and filters for Lab 5 rules 100501–100505. By default, it sends each new alert to a local Mailpit inbox at `http://localhost:8025`, which provides screenshot evidence without delivering mail outside the VM. For actual email delivery, replace the default variables by creating an untracked `.env` file in the project root:

```dotenv
SMTP_HOST=smtp.example.edu
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USER=your-account
SMTP_PASSWORD=your-app-password
ALERT_FROM=lab5@example.edu
ALERT_TO=student@example.edu
```

Start or refresh the service after configuring the values:

```sh
docker compose -p lab5 -f vendor/wazuh-docker/single-node/docker-compose.yml -f docker-compose.lab5.yml up -d alert-notifier
```

Watch delivery status with `docker logs -f lab5-alert-notifier`, replay the events, and confirm that one message arrives per matching rule. Protect `.env`; never commit real credentials. The notifier starts at the end of the existing alert file, so it only sends notifications for newly generated events.

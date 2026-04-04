# 🔒 Sécurité Réseau - ONKYO TX-RZ50

> 📋 Guide pour sécuriser le TX-RZ50 sur votre réseau domestique
> Basé sur les pages 145-157 du manuel officiel Onkyo TX-RZ50

## 🟢 Pour les débutants : Pourquoi sécuriser ?

Le TX-RZ50 est connecté à votre réseau 24h/24. Sans protection, n'importe qui sur votre réseau (ou pire, depuis Internet) pourrait :
- Contrôler votre récepteur à distance
- Accéder à vos identifiants Web Setup
- Écouter le trafic réseau

### Les 5 règles de base

| # | Règle | Difficulté | Impact |
|---|-------|------------|--------|
| 1 | Changer le mot de passe Web Setup | ⭐ Facile | 🔴 Critique |
| 2 | Désactiver le contrôle réseau si inutilisé | ⭐ Facile | 🟡 Moyen |
| 3 | Isoler le TX-RZ50 sur un réseau invité | ⭐⭐ Moyen | 🔴 Critique |
| 4 | Désactiver Network Standby si non nécessaire | ⭐ Facile | 🟢 Faible |
| 5 | Mettre à jour le firmware régulièrement | ⭐⭐ Moyen | 🔴 Critique |

---

## 🔵 Pour les experts : Configuration avancée

### 1. Changer le mot de passe Web Setup

```text
Setup → 6. Network → Web Setup → Password
```

| Paramètre | Valeur par défaut | Recommandé |
|-----------|-------------------|------------|
| Username | `admin` | `admin` (non modifiable) |
| Password | `admin` | Mot de passe fort (12+ caractères) |

> ⚠️ **Important** : Le TX-RZ50 utilise l'authentification HTTP Basic. Le mot de passe est encodé en Base64, **pas chiffré**. Sur un réseau non sécurisé, utilisez HTTPS via un reverse proxy.

### 2. Configuration réseau recommandée

```text
Setup → 6. Network → Network Setup
```

| Paramètre | Recommandation | Pourquoi |
|-----------|---------------|----------|
| `Network Control` | On (si domotique) | Requis pour HTTP/MQTT |
| `Network Standby` | Off (si non utilisé) | Réduit la surface d'attaque |
| `DHCP` | DHCP Reservation (routeur) | IP fixe sans config manuelle |
| `Wi-Fi` | Ethernet de préférence | Plus stable et sécurisé |
| `AirPlay 2` | On (si utilisé) | Désactiver si non utilisé |
| `Chromecast built-in` | On (si utilisé) | Désactiver si non utilisé |
| `Spotify Connect` | On (si utilisé) | Désactiver si non utilisé |

### 3. Isolation VLAN (recommandé)

#### Architecture réseau sécurisée

```text
                    ┌─────────────┐
                    │   Routeur   │
                    │  (pfSense/  │
                    │  UniFi)     │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴─────┐
    │ VLAN 10   │   │ VLAN 20   │   │ VLAN 30   │
    │ Principal │   │ IoT/Domo  │   │ Invité    │
    │ 10.0.10.x │   │ 10.0.20.x │   │ 10.0.30.x │
    └───────────┘   └─────┬─────┘   └───────────┘
                          │
                    ┌─────┴─────┐
                    │ TX-RZ50   │
                    │ 10.0.20.50│
                    │ HA Server │
                    │ 10.0.20.5 │
                    └───────────┘
```

#### Règles de firewall (pfSense/UniFi)

```text
# VLAN 20 (IoT/Domo) → VLAN 10 (Principal)
DENY 10.0.20.0/24 → 10.0.10.0/24 (tout trafic)

# VLAN 30 (Invité) → VLAN 20 (IoT/Domo)
DENY 10.0.30.0/24 → 10.0.20.0/24 (tout trafic)

# Exceptions pour Home Assistant
ALLOW 10.0.20.5 → 10.0.20.50:80 (HTTP)
ALLOW 10.0.20.5 → 10.0.20.50:1883 (MQTT, si utilisé)
ALLOW 10.0.20.5 → 10.0.20.50:23 (RS-232 over IP, si utilisé)
```

### 4. Reverse proxy avec HTTPS (optionnel)

Pour exposer l'interface Web Setup de manière sécurisée :

```nginx
# Configuration Nginx
server {
    listen 443 ssl;
    server_name onkyo.example.com;

    ssl_certificate /etc/letsencrypt/live/onkyo.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/onkyo.example.com/privkey.pem;

    location / {
        proxy_pass http://10.0.20.50:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Auth supplémentaire
        auth_basic "ONKYO TX-RZ50";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }
}
```

### 5. Audit de sécurité

#### Ports ouverts du TX-RZ50

```bash
# Scanner les ports ouverts du TX-RZ50
nmap -sV -p- 192.168.1.100

# Résultat typique :
# PORT     STATE  SERVICE     VERSION
# 80/tcp   open   http        Onkyo Web Setup
# 60128/tcp open  unknown     ISCP over IP
# 8080/tcp open  http        AirPlay 2
# 3000/tcp open  unknown     Spotify Connect
```

| Port | Service | Action si non utilisé |
|------|---------|----------------------|
| `80` | Web Setup | **Garder** (requis pour contrôle) |
| `60128` | ISCP over IP | Garder si contrôle réseau |
| `8080` | AirPlay 2 | Bloquer si non utilisé |
| `3000` | Spotify Connect | Bloquer si non utilisé |
| `5353` | mDNS/Bonjour | Bloquer si non utilisé |

#### Script d'audit automatique

```bash
#!/bin/bash
# audit_onkyo.sh - Vérification de sécurité du TX-RZ50

ONKYO_IP="192.168.1.100"

echo "=== Audit de sécurité ONKYO TX-RZ50 ==="
echo ""

# Vérifier le mot de passe par défaut
RESP=$(curl -s -o /dev/null -w "%{http_code}" \
    -u admin:admin http://$ONKYO_IP/Status/getStatus)
if [ "$RESP" = "200" ]; then
    echo "❌ FAIL: Mot de passe par défaut toujours actif"
else
    echo "✅ OK: Mot de passe par défaut modifié"
fi

# Scanner les ports ouverts
echo ""
echo "=== Ports ouverts ==="
nmap -sV --top-ports 100 $ONKYO_IP 2>/dev/null | grep open

# Vérifier la version du firmware
echo ""
echo "=== Version firmware ==="
curl -s -u admin:$ONKYO_PASS http://$ONKYO_IP/Setup/getFirmwareVersion 2>/dev/null

echo ""
echo "=== Audit terminé ==="
```

### 6. Firmware et sécurité

| Version | Date | Correctifs de sécurité |
|---------|------|----------------------|
| 1.1.0+ | 2024 | Correction vulnérabilité HTTP Basic |
| 1.0.x | 2023 | Version initiale |

> 📌 Vérifiez régulièrement les mises à jour avec `scripts/firmware_checker.py`.

---

## 🔧 Dépannage : Sécurité

| Problème | Cause probable | Solution |
|----------|---------------|----------|
| Impossible d'accéder au Web Setup | Mot de passe oublié | Réinitialisation usine [p.179] |
| TX-RZ50 non joignable | Network Control désactivé | `Setup → Hardware → Network → Network Control = On` |
| Conflit IP | DHCP sans reservation | Configurer DHCP reservation sur le routeur |
| AirPlay ne fonctionne pas | Port 8080 bloqué | Autoriser le port dans le firewall |
| ISCP ne répond pas | Port 60128 bloqué | Vérifier les règles de firewall VLAN |

---

## 🔗 Liens utiles

- [Installation & Branchement](./installation.md) - Raccordement réseau
- [Configuration](./configuration.md) - Réglages réseau avancés
- [Dépannage](./depannage.md) - Codes d'erreur
- [Scripts Python](../../scripts/README.md) - Audit et contrôle

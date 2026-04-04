# 🌐 Multizone - ZONE 2 & ZONE 3

> 📋 Basé sur le manuel officiel Onkyo TX-RZ50 [p.108-111]

## 🟢 Pour les débutants : Qu'est-ce que le Multizone ?

Le Multizone permet de diffuser du son dans **plusieurs pièces** de votre maison, indépendamment de la zone principale (ZONE 1). Le TX-RZ50 gère jusqu'à **3 zones** simultanément :

| Zone | Description | Usage typique |
|------|-------------|---------------|
| **ZONE 1** | Salon / pièce principale | Home-cinéma, écoute principale |
| **ZONE 2** | Deuxième pièce (chambre, cuisine) | Musique d'ambiance, radio |
| **ZONE 3** | Troisième pièce (terrasse, bureau) | Son léger, podcasts |

### Comment ça fonctionne ?

```text
                    TX-RZ50
                   /   |   \
                  /    |    \
           ZONE 1  ZONE 2  ZONE 3
          (Salon)  (Cuisine) (Terrasse)
         5.1.2ch    2.0ch     2.0ch
```

- Chaque zone peut avoir sa **propre source** et son **propre volume**
- ZONE 2 et ZONE 3 utilisent des **amplificateurs dédiés** qui réduisent le nombre de canaux disponibles pour ZONE 1
- Les enceintes des zones secondaires se branchent sur les **bornes SPEAKERS ZONE 2** à l'arrière

---

## 🔌 Raccordement des zones secondaires

### ZONE 2

```text
TX-RZ50 [SPEAKERS ZONE 2 L/R] ──Câbles enceintes──▶ Enceintes stéréo ZONE 2
```

| Paramètre | Détail |
|-----------|--------|
| Bornes | `ZONE 2 L` et `ZONE 2 R` (panneau arrière) |
| Impédance | 4 Ω à 16 Ω [p.108] |
| Canaux | Stéréo (2.0) |
| Sources disponibles | **HDMI 1-3 uniquement** + sources numériques/analogiques [p.109] |

### ZONE 3

```text
TX-RZ50 [ZONE 3 OUT L/R] ──Câbles RCA──▶ Ampli externe ──▶ Enceintes ZONE 3
```

| Paramètre | Détail |
|-----------|--------|
| Sortie | `ZONE 3 OUT L/R` (RCA, panneau arrière) |
| Type | Sortie ligne (nécessite un ampli externe) |
| Canaux | Stéréo (2.0) |
| Sources | **Câble audio analogique uniquement** [p.110] |

> ⚠️ **Important** : ZONE 3 ne fonctionne qu'avec des sources analogiques. Les sources HDMI et numériques ne sont **pas** disponibles pour ZONE 3.

---

## 🔵 Pour les experts : Configuration avancée

### Impact sur la configuration des enceintes ZONE 1

Lorsque ZONE 2 est activée, les canaux d'amplification sont redistribués :

| Configuration ZONE 1 | ZONE 2 activée | Résultat |
|---------------------|----------------|----------|
| 9.2 ch | ❌ Impossible | ZONE 2 nécessite 2 canaux |
| 7.1.2 ch | ✅ Possible | Surround Back + Height disponibles |
| 5.1.2 ch | ✅ Possible | Configuration optimale |
| 5.1 ch | ✅ Possible | Tous les canaux disponibles |

> 📌 **Règle** : Chaque zone active consomme 2 canaux d'amplification. Le TX-RZ50 dispose de 9 canaux au total [p.108].

### Configuration via le menu Setup

```text
Setup → 4. Zone → Zone 2 Setup / Zone 3 Setup
```

#### Zone 2 Setup

| Paramètre | Options | Description |
|-----------|---------|-------------|
| `Zone 2` | On / Off | Active/désactive ZONE 2 |
| `Zone 2 Source` | BD/DVD, NET, BT, etc. | Sélectionne la source [p.109] |
| `Zone 2 Volume` | 0-80 | Niveau sonore |
| `Zone 2 Max Volume` | 0-80 | Limite supérieure (protection) |
| `Zone 2 Fixed Volume` | On / Off | Volume fixe (bypass télécommande) |

#### Zone 3 Setup

| Paramètre | Options | Description |
|-----------|---------|-------------|
| `Zone 3` | On / Off | Active/désactive ZONE 3 |
| `Zone 3 Source` | Sources analogiques uniquement | Sélectionne la source [p.110] |
| `Zone 3 Volume` | 0-80 | Niveau sonore |

### Limitations importantes

| Limitation | Détail | Référence |
|------------|--------|-----------|
| `Pure Audio` + Multizone | Incompatibles → bascule auto en `Direct` | [p.111] |
| ZONE 2 HDMI | Sources HDMI 1-3 uniquement (pas 4-6) | [p.109] |
| ZONE 3 numérique | Non supporté, analogique uniquement | [p.110] |
| DSD/NET vers ZONE 2/3 | Non supporté → forcer PCM 2ch sur la source | [p.109-111] |
| Dirac Live | Désactivé pour les zones secondaires | [p.166] |
| Consommation veille | Augmente si ZONE 2/3 actif en veille | [p.109-111] |

---

## 🎛️ Contrôle des zones

### Via la télécommande

1. Appuyer sur la touche **ZONE 2** ou **ZONE 3** de la télécommande
2. Utiliser les touches de source pour changer l'entrée
3. Régler le volume avec les touches `VOLUME ▲/▼`

### Via RS-232 (ISCP)

```bash
# ZONE 2 - Allumer
python rs232_control.py --port COM3 --command "ZONE2 POWER_ON"

# ZONE 2 - Éteindre
python rs232_control.py --port COM3 --command "ZONE2 POWER_OFF"

# ZONE 2 - Changer la source
python rs232_control.py --port COM3 --command "ZONE2 SOURCE BLUETOOTH"

# ZONE 2 - Régler le volume (0-80)
python rs232_control.py --port COM3 --command "ZONE2 VOLUME 30"
```

### Via HTTP API

```bash
# ZONE 2 - Allumer
python http_api_wrapper.py --host 192.168.1.100 --action zone2_power --state on

# ZONE 2 - Volume
python http_api_wrapper.py --host 192.168.1.100 --action zone2_volume --level 35
```

### Via Home Assistant

Voir [config/home_assistant.yaml](../../config/home_assistant.yaml) pour la configuration REST/MQTT complète.

---

## 📊 Scénarios d'usage courants

### Scénario 1 : Soirée cinéma + musique dans la cuisine

```text
ZONE 1 (Salon)  : Source = BD/DVD    | Mode = Dolby Atmos  | Volume = 55
ZONE 2 (Cuisine): Source = NET       | Mode = Stereo       | Volume = 30
ZONE 3          : Off
```

### Scénario 2 : Radio matinale dans toute la maison

```text
ZONE 1 (Salon)  : Source = TUNER     | Mode = Stereo       | Volume = 35
ZONE 2 (Cuisine): Source = TUNER     | Mode = Stereo       | Volume = 25
ZONE 3 (Terrasse): Source = TUNER    | Mode = Stereo       | Volume = 30
```

### Scénario 3 : Gaming dans le salon, ambiance sur la terrasse

```text
ZONE 1 (Salon)  : Source = GAME      | Mode = Game-Action  | Volume = 50
ZONE 2          : Off
ZONE 3 (Terrasse): Source = BLUETOOTH| Mode = Stereo       | Volume = 35
```

---

## 🔧 Dépannage rapide : Multizone

| Problème | Cause probable | Solution |
|----------|---------------|----------|
| Pas de son en ZONE 2 | Source HDMI 4-6 sélectionnée | Utiliser HDMI 1-3 uniquement [p.109] |
| ZONE 3 muette | Source numérique sélectionnée | Basculer sur une source analogique [p.110] |
| Volume ZONE 2 bloqué | `Max Volume` ou `Fixed Volume` activé | Ajuster dans `Setup → Zone → Zone 2 Setup` |
| `Pure Audio` grisé | ZONE 2 ou ZONE 3 activée | Désactiver les zones secondaires [p.111] |
| Son DSD coupé en ZONE 2 | Format DSD non supporté en zone secondaire | Forcer la sortie PCM 2ch sur la source [p.109] |
| Consommation veille élevée | Network Standby + ZONE 2/3 actif | Désactiver les zones en veille [p.109-111] |

---

## 🔗 Liens utiles

- [Installation & Branchement](./installation.md) - Raccordement des enceintes
- [Configuration & Calibration](./configuration.md) - AccuEQ, Dirac Live
- [Modes d'écoute](./modes_ecoute.md) - Dolby Atmos, DTS:X, THX
- [Dépannage](./depannage.md) - Codes d'erreur et solutions
- [Scripts Python](../../scripts/README.md) - Contrôle automatisé

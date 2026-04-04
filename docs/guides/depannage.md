# 🛠️ Dépannage & Codes d'erreur

> 📋 Basé sur le manuel officiel Onkyo TX-RZ50 [p.169-181]

## 🟢 Pour les débutants : Diagnostic rapide

### Flux de résolution en 3 étapes
1. **Redémarrage** : Mets l'appareil en veille (`ON/STANDBY`), attends 5 secondes, puis rallume-le [p.170].
2. **Vérification câbles** : Débranche/rebranche les câbles HDMI, enceintes et alimentation. Vérifie qu'aucun fil dénudé ne touche une borne métallique [p.171].
3. **Réinitialisation** : Si le problème persiste, effectue un **Factory Reset** (voir section Expert ci-dessous) [p.170].

### Symptômes courants & Solutions immédiates
| Problème | Vérification rapide | Action |
|----------|-------------------|--------|
| 🔇 Pas de son | `MUTE` activé ? Casque branché ? | Appuie sur `MUTE` ou débranche le casque [p.171] |
| 📺 Pas d'image | Entrée TV correcte ? Mode `Pure Audio` activé ? | Change l'entrée TV. Désactive `Pure Audio` (nécessite un circuit vidéo) [p.174] |
| 🔊 Son haché / coupures | Câbles groupés ? Interférences ? | Éloigne les câbles audio des cordons d'alimentation [p.173] |
| 🌐 Pas de connexion réseau | Voyant `NET` clignote ? | Redémarre routeur + TX-RZ50. Vérifie le câble Ethernet [p.178] |

---

## 🔵 Pour les experts : Procédures avancées

### 🔴 Codes d'erreur critique
| Code | Signification | Résolution technique | Référence |
|------|--------------|---------------------|-----------|
| `AMP Diag Mode` | Circuit de protection activé | Vérifie les courts-circuits sur les bornes enceintes. Si `CH SP WIRE` → isole les fils. Si `NG:` → débranche immédiatement, contacte SAV [p.171] | [p.171] |
| `**-01` / `**-10` | Câble Ethernet / USB non détecté | Rebranche fermement. Vérifie le format FAT16/32 pour USB [p.9-10] | [p.9-10] |
| `Resolution Error` | Résolution vidéo non supportée | Change la résolution de sortie du lecteur. Désactive `Deep Color` si scintillement [p.175] | [p.175] |
| `Noise Error` | Interférence pendant AccuEQ | Vérifie le micro, réduis les bruits ambiants, baisse le volume du sub avant calibration [p.181] | [p.181] |

### 🔧 Réinitialisation d'usine (Factory Reset)
> ⚠️ **Attention** : Efface tous les réglages personnalisés. Note-les avant [p.170].
```powershell
# Procédure matérielle
1. Appareil allumé → maintiens `CBL` + appuie sur `ON/STANDBY`
2. L'écran affiche `Clear` → attends la disparition du message
3. L'appareil retourne en veille → rallume-le normalement
```
*Réinitialisation télécommande* : Maintiens `MODE` + `CLEAR` pendant 3 secondes [p.170].

### 🎛️ Bascule Deep Color (si scintillement HDMI)
```powershell
# Procédure clavier frontal
Maintiens `STM` + appuies successivement sur `ON/STANDBY` jusqu'à afficher `Deep Color:Off` (ou `:On`) [p.175]
```

### 📡 Problèmes HDMI CEC / Liaison
- Si les commandes liées échouent : `Setup → 5. Hardware → HDMI → HDMI CEC = Off`, puis remets sur `On` [p.175].
- Pour les appareils Sharp : règle `HDMI Standby Through = Auto` [p.175].
- Limite CEC : max 3 lecteurs/enregistreurs + 4 tuners branchés en chaîne [p.206].

### 🌐 Réseau & Bluetooth
| Problème | Solution experte |
|----------|-----------------|
| Appairage BT impossible | `Setup → 5. Hardware → Bluetooth → [Receiver/Transmitter] → Pairing Information → Clear` [p.176-177] |
| Wi-Fi ne voit pas le SSID | Routeur en mode "masqué" ? Change en SSID visible. Caractères multi-octets ? Passe en alphanumérique 1-octet [p.179] |
| Audio DSD/NET vers ZONE 2/3 | Non supporté. Force la sortie PCM 2ch sur la source externe [p.109-111] |
| Chromecast/Alexa en conflit | Désactive l'un des deux dans `5. Hardware → Network` [p.145] |

### 🎛️ Limitations Multizone
- `ZONE 2` : Sources HDMI 1-3 uniquement. Son analogique ou PCM 2ch max [p.109].
- `ZONE 3` : Uniquement câble audio analogique. Pas de HDMI/numérique [p.110].
- `Pure Audio` + `Multizone` incompatibles → bascule auto en `Direct` [p.111].
- Consommation veille augmente si ZONE 2/3 actif [p.109-111].

---

## 📊 Checklist de maintenance préventive
- [ ] Mise à jour firmware vérifiée (`7. Miscellaneous → Firmware Update → Version`) [p.156]
- [ ] Câbles HDMI `Premium High Speed` (4K) ou `ULTRA High Speed` (8K) [p.62]
- [ ] Impédance enceintes vérifiée (`4ohms` si <6Ω) [p.132]
- [ ] Micro calibration débranché après AccuEQ/Dirac [p.171]
- [ ] Espace ventilation ≥10 cm respecté [p.171]

---

[⬅️ Retour au README](../../README.md) | [⏭️ Suite : Guides Markdown complémentaires](./modes_ecoute.md)

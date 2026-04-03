# 🔧 Installation & Branchement

> 📋 Basé sur le manuel officiel Onkyo TX-RZ50 [p.7-77]

## 🟢 Pour les débutants : Premiers pas en toute sécurité

### Avant de commencer
- ✅ **Branchements d'abord** : Effectuez toutes les connexions (enceintes, HDMI, antennes) **avant** de brancher le cordon d'alimentation [p.7].
- ✅ **Impédance des enceintes** : Utilisez des enceintes de 4 Ω à 16 Ω [p.39].
- ✅ **Ventilation** : Laissez au moins 10 cm d'espace autour de l'appareil pour éviter la surchauffe [p.171].

### Branchement des enceintes (Système 5.1 de base)
```text
        FL      FR
          \    /
           \  /
            C
           /  \
          /    \
        SL      SR
            SW
```

| Enceinte | Position recommandée |
|----------|---------------------|
| FL/FR (Avant) | À hauteur d'oreille, 22°-30° par rapport à l'écoute |
| C (Centrale) | Face à la position d'écoute, au-dessus/au-dessous de l'écran |
| SL/SR (Surround) | Juste au-dessus de la hauteur d'oreille, 120° latéral |
| SW (Subwoofer) | Entre la centrale et une enceinte avant |

> ⚠️ **Attention** : Entortillez les fils dénudés des câbles d'enceinte pour qu'ils ne dépassent pas des bornes. Un court-circuit peut activer le circuit de protection [p.39].

## 🔵 Pour les experts : Gestion thermique et consommation

### Consommation en mode veille
| Fonction activée | Consommation approximative |
|-----------------|---------------------------|
| Full Standby (tout éteint) | 0,1 W |
| HDMI CEC activé | +0,05 W |
| Network Standby activé | ~1,7 W |
| Bluetooth Wakeup activé | ~1,6 W |
| **TOUT activé (HiNA)** | **2,7-2,8 W** [p.208] |

### Circuit de protection : Messages d'erreur critiques
| Message | Cause probable | Action immédiate |
|---------|---------------|-----------------|
| `AMP Diag Mode` | Température interne élevée ou court-circuit | Vérifier ventilation, débrancher 5 min [p.171] |
| `CH SP WIRE` | Court-circuit sur bornes enceintes | Vérifier câblage, entortiller les fils [p.171] |
| `NG: XXXXX` | Défaillance matérielle interne | **Débrancher immédiatement**, contacter SAV [p.171] |

### Mise à jour Firmware : Précautions
- ⏱️ Durée : ~20 minutes via réseau ou USB [p.8]
- 🔌 **Ne jamais couper l'alimentation** pendant la mise à jour
- 📡 Désactiver HDMI CEC avant une mise à jour réseau [p.8]
- 💾 Sauvegarder vos réglages personnalisés avant la mise à jour

---

## 🔗 Raccordements HDMI & Audio

### Vers un téléviseur ARC/eARC
```text
TX-RZ50 [HDMI OUT MAIN (ARC)] ──HDMI──▶ TV [HDMI IN (ARC)]
```
- ✅ Un seul câble HDMI suffit pour audio + vidéo + commande CEC [p.63]
- ✅ Pour eARC : utiliser un câble HDMI "High Speed with Ethernet" [p.63]

### Vers un téléviseur NON-ARC
```text
TX-RZ50 [HDMI OUT MAIN] ──HDMI──▶ TV [HDMI IN]
TX-RZ50 [DIGITAL OUT OPTICAL] ──Optique──▶ TV [DIGITAL IN]
```
- 🔊 Le son de la TV vers les enceintes nécessite un câble optique ou analogique supplémentaire [p.63]

### Câbles HDMI recommandés
| Résolution cible | Type de câble requis | Bande passante |
|-----------------|---------------------|----------------|
| 4K 30Hz / HDR10 | Premium High Speed | 18 Gbps |
| 4K 60Hz / HDR10+ | Premium High Speed | 18 Gbps |
| 8K 60Hz / VRR | ULTRA High Speed | 48 Gbps |

> 📌 **Astuce** : Les entrées HDMI 1-3 du TX-RZ50 supportent 40 Gbps (8K/60p). Les entrées 4-6 sont limitées à 24 Gbps (8K/24p) [p.204].

---

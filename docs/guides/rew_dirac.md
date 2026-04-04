# 🎯 Guide REW + Dirac Live - Calibration avancée

> 📋 Tutoriel pour calibrer le Dirac Live du TX-RZ50 avec Room EQ Wizard (REW)
> Basé sur les pages 160-166 du manuel officiel Onkyo TX-RZ50

## 🟢 Pour les débutants : Pourquoi calibrer ?

Le **Dirac Live** est un système de correction acoustique qui analyse votre pièce et ajuste automatiquement le son pour compenser les défauts (résonances, annulations de phase, déséquilibres). Mais les cibles par défaut ne sont pas toujours optimales.

**Room EQ Wizard (REW)** est un logiciel gratuit qui permet de :
- Mesurer la réponse en fréquence de chaque enceinte
- Visualiser les problèmes acoustiques de la pièce
- Définir une **courbe cible personnalisée** pour Dirac Live
- Comparer avant/après correction

### Ce dont vous avez besoin

| Élément | Description |
|---------|-------------|
| 🎤 Micro de mesure | UMIK-1 (recommandé) ou miniDSP UMIK-2 |
| 💻 PC/Mac | Avec REW installé (gratuit) |
| 🔌 Câble USB | Pour connecter le micro au PC |
| 📐 Trépied | Pour placer le micro à hauteur d'oreille |
| 📱 TX-RZ50 | Avec licence Dirac Live activée [p.160] |

---

## 🔵 Pour les experts : Workflow complet

### Étape 1 : Préparation de la pièce

```text
1. Éteindre la climatisation / ventilation
2. Fermer portes et fenêtres
3. Placer le micro à hauteur d'oreille (position d'écoute principale)
4. Connecter le micro UMIK-1 au PC via USB
5. Charger le fichier de calibration du micro dans REW
   (fichier .txt fourni avec le UMIK-1)
```

### Étape 2 : Configuration du TX-RZ50 pour Dirac Live

```text
Setup → 2. Speaker → Dirac Live
```

| Paramètre | Valeur recommandée | Référence |
|-----------|-------------------|-----------|
| `Dirac Live` | On | [p.160] |
| `Microphone Type` | UMIK-1 (USB) | [p.161] |
| `Measurement Points` | 9 points (recommandé) | [p.162] |
| `Subwoofer Mode` | LFE + Main (si double sub) | [p.163] |
| `Bass Control` | Activé (pour correction sub) | [p.164] |

### Étape 3 : Mesures REW avant Dirac

#### Configuration REW

```text
Preferences → Audio → Device:
  - Output: Carte son connectée à l'entrée LINE du TX-RZ50
  - Input: UMIK-1 (USB)
  - Sample rate: 48000 Hz
  - Buffer size: 4096
```

#### Procédure de mesure

1. **Configurer le TX-RZ50** : Source = ligne, volume = -20 dB, mode = Direct
2. **Générer le signal** : REW → Generator → Sweep → 20 Hz - 20 kHz
3. **Mesurer chaque enceinte** individuellement :
   ```
   Mesure 1 : Enceinte avant gauche
   Mesure 2 : Enceinte avant droite
   Mesure 3 : Centrale
   Mesure 4 : Surround gauche
   Mesure 5 : Surround droite
   Mesure 6 : Height gauche
   Mesure 7 : Height droite
   Mesure 8 : Subwoofer
   ```
4. **Sauvegarder les mesures** : File → Save all measurements as...

### Étape 4 : Analyse des résultats REW

#### Indicateurs clés

| Indicateur | Bon | Problématique | Action |
|------------|-----|---------------|--------|
| **Réponse 20-200 Hz** | ±6 dB | > ±10 dB | Repositionner sub/enceintes |
| **Réponse 200 Hz-20 kHz** | ±4 dB | > ±8 dB | Ajouter traitement acoustique |
| **Waterfall decay** | < 300 ms | > 500 ms | Panneaux absorbants |
| **RT60** | 0.3-0.5 s | > 0.7 s | Traitement acoustique prioritaire |

#### Commandes REW utiles

```text
# All overlay : comparer toutes les mesures
Graph Controls → All SPL → Overlay

# Waterfall : visualiser la décroissance
Waterfall → Settings → Resolution: 256, Window: 500 ms

# RT60 : temps de réverbération
RT60 → Settings → Decay range: 60 dB
```

### Étape 5 : Définir la courbe cible pour Dirac

#### Courbes recommandées par usage

**🎬 Cinéma (Harman target)**
```text
Fréquence    | Niveau relatif
-------------|---------------
20 Hz        | 0 dB
100 Hz       | 0 dB
500 Hz       | -2 dB
2 kHz        | -4 dB
10 kHz       | -6 dB
20 kHz       | -8 dB
```
*Pente douce de -8 dB entre 500 Hz et 20 kHz pour un son naturel.*

**🎵 Musique (Flat)**
```text
Fréquence    | Niveau relatif
-------------|---------------
20 Hz - 20 kHz | 0 dB (plat)
```
*Réponse plate pour une écoute fidèle.*

**🎸 Rock / Jazz (Warm)**
```text
Fréquence    | Niveau relatif
-------------|---------------
20 Hz        | +2 dB
100 Hz       | +1 dB
500 Hz       | 0 dB
2 kHz        | -1 dB
10 kHz       | -3 dB
20 kHz       | -5 dB
```
*Léger boost dans les graves, douceur dans les aigus.*

### Étape 6 : Exécuter Dirac Live avec la courbe cible

1. **Lancer l'assistant Dirac** sur le TX-RZ50 : `Setup → 2. Speaker → Dirac Live → Start`
2. **Effectuer les 9 mesures** selon les positions indiquées :
   ```text
   Position 1 : Écoute principale (micro hauteur oreille)
   Position 2 : 30 cm à gauche de P1
   Position 3 : 30 cm à droite de P1
   Position 4 : 30 cm en avant de P1
   Position 5 : 30 cm en arrière de P1
   Position 6 : Canapé gauche (si applicable)
   Position 7 : Canapé droit (si applicable)
   Position 8 : Position secondaire
   Position 9 : Position secondaire
   ```
3. **Importer la courbe cible** dans l'interface Dirac [p.164]
4. **Appliquer la correction** et sauvegarder

### Étape 7 : Vérification post-calibration

#### Mesures REW après Dirac

1. Refaire les mêmes mesures qu'à l'étape 3
2. Superposer avec les mesures "avant" dans REW
3. Vérifier les améliorations :

```text
✅ Réponse en fréquence : ±3 dB sur 20 Hz - 20 kHz
✅ Decay waterfall : < 200 ms sous 200 Hz
✅ Phase : cohérente entre enceintes
✅ Subwoofer : transition fluide avec les satellites (80 Hz)
```

---

## 📊 Optimisation Subwoofer

### Double subwoofer (2 subs)

| Paramètre | Réglage | Pourquoi |
|-----------|---------|----------|
| `Crossover` | 80 Hz (THX standard) | Transition optimale sub/satellites |
| `Phase` | 0° ou 180° (tester les deux) | Annulation constructive |
| `Level` | Égaliser les deux subs au SPL-mètre | Réponse uniforme |
| `Position` | Coins opposés ou milieu des murs | Réduire les modes propres |

### Technique du "sub crawl"

```text
1. Placer le subwoofer à la position d'écoute principale
2. Jouer un signal de test (sweep 20-80 Hz ou musique avec basses)
3. Se déplacer à quatre pattes dans la pièce
4. Identifier l'endroit où les basses sont les plus équilibrées
5. Placer le subwoofer à cet endroit
```

---

## 🔧 Dépannage : Dirac Live

| Problème | Cause probable | Solution |
|----------|---------------|----------|
| `Dirac Live` grisé | Licence non activée | Acheter/activer la licence [p.160] |
| Mesure échoue | Micro non détecté | Vérifier connexion USB, charger fichier calibration |
| Réponse irrégulière après calibration | Courbe cible trop agressive | Réduire la pente, viser ±6 dB max |
| Sub non corrigé | Bass Control désactivé | Activer dans `Setup → Speaker → Dirac → Bass Control` [p.164] |
| Bruit pendant mesure | Interférence ambiante | Couper clim, fermer fenêtres, silence |
| Dirac désactivé en ZONE 2/3 | Limitation matérielle | Normal, Dirac ne fonctionne que sur ZONE 1 [p.166] |

---

## 🔗 Liens utiles

- [Configuration & Calibration](./configuration.md) - AccuEQ, réglages audio
- [Multizone](./multizone.md) - ZONE 2/3
- [Modes d'écoute](./modes_ecoute.md) - Dolby Atmos, DTS:X, THX
- [Dépannage](./depannage.md) - Codes d'erreur
- [REW](https://www.roomeqwizard.com/) - Site officiel
- [Dirac Live](https://dirac.se/dirac-live/) - Site officiel

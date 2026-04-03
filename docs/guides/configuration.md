# ⚙️ Configuration & Calibration

> 📋 Basé sur le manuel officiel Onkyo TX-RZ50 [p.124-167, p.192-198]

## 🟢 Pour les débutants : Calibration automatique simplifiée

### AccuEQ Room Calibration (recommandé pour débuter)
AccuEQ est la technologie de calibration automatique intégrée au TX-RZ50. Elle mesure l'acoustique de ta pièce et ajuste automatiquement :
- Le niveau de chaque enceinte
- La distance entre chaque enceinte et la position d'écoute
- La fréquence de crossover
- L'égalisation pour compenser les réflexions et ondes stationnaires

#### Procédure pas-à-pas :
1. Branche le **microphone de configuration** fourni à la prise `SETUP MIC` (panneau avant) [p.12, p.161]
2. Place le micro sur un trépied à hauteur d'oreille, à ta position d'écoute principale
3. Va dans `Setup` → `Initial Setup` → `Room EQ` → `AccuEQ Room Calibration` [p.158-160]
4. Suis les instructions à l'écran : l'appareil émettra des tonalités de test via chaque enceinte
5. Une fois la mesure terminée, l'appareil applique automatiquement les réglages optimaux

> ⚠️ **Conseils pour une mesure précise** :
> - Éteins les climatiseurs, ventilateurs, et réduis les bruits ambiants
> - Personne ne doit bouger dans la pièce pendant la mesure
> - Régle le volume du caisson de basse à ~50% avant de commencer [p.160]

### Dirac Live (pour audiophiles)
Dirac Live est une technologie de correction de salle avancée (payante, via l'app Onkyo Controller) qui offre :
- Une correction de la réponse impulsionnelle (pas seulement fréquentielle)
- Jusqu'à 3 profils de calibration sauvegardables
- Un réglage manuel fin des courbes d'égalisation

#### Prérequis :
- Smartphone/tablet avec l'app **Onkyo Controller** (iOS/Android) [p.164]
- Connexion Wi-Fi entre l'app et le TX-RZ50
- Licence Dirac Live (achat in-app)

#### Procédure rapide :
1. Lance Onkyo Controller et connecte-toi au TX-RZ50
2. Va dans le menu `Dirac Live` et suis le guide de mesure
3. Choisis entre :
   - `Quick` : 3 positions de mesure (centre, gauche, droite)
   - `Full` : 9 positions pour une couverture optimale [p.161-162]
4. Transfère les résultats vers le TX-RZ50

> 💡 **Astuce** : Dirac Live désactive les réglages manuels de distance (affichés en `msec`), mais tu peux toujours ajuster finement l'égaliseur via le mode `Manual Adjust` dans l'app [p.166-167].

---

## 🔵 Pour les experts : Réglages audio avancés

### Fréquences de crossover (Crossover Settings)
Le crossover détermine à partir de quelle fréquence les basses sont redirigées vers le caisson de basse.

| Enceinte | Réglage recommandé | Quand modifier |
|----------|-------------------|----------------|
| Avant (Front) | `80 Hz (THX)` | Enceintes certifiées THX ou petites enceintes satellites |
| Centrale | `80 Hz (THX)` | Pour une intégration fluide avec les avant |
| Surround | `80-100 Hz` | Enceintes surround compactes |
| Surround Back | `80-100 Hz` | Si utilisées |
| Height 1/2 | `80-120 Hz` | Enceintes en hauteur ou Dolby Atmos |
| LPF of LFE | `120 Hz` | Filtre passe-bas pour le canal LFE (effets basses) |
| Double Bass | `Off` (recommandé) | Évite la surcharge des basses si les avant sont "Small" [p.133] |

> 📌 **Règle THX** : Pour des enceintes certifiées THX, utilise :
> - Crossover : `80 Hz (THX)`
> - LPF of LFE : `80 Hz`
> - Double Bass : `Off` [p.133, p.197]

### Réglage des distances (Distance Calibration)
Après une calibration AccuEQ ou Dirac Live, les distances sont automatiquement mesurées. Tu peux les ajuster manuellement si nécessaire :

```powershell
# Exemple de réglage manuel (via menu Setup)
Setup → 2. Speaker → 3. Distance
```

| Enceinte | Distance typique | Unité |
|----------|-----------------|-------|
| Avant | 2.5 - 4.0 m | mètres |
| Centrale | 2.5 - 4.0 m | mètres |
| Surround | 2.0 - 3.5 m | mètres |
| Caisson de basse | 2.5 - 4.0 m | mètres |

> ⚠️ **Note** : Après une calibration Dirac Live, les distances sont affichées en `msec` (millisecondes) et ne sont plus modifiables manuellement [p.134, p.162].

### Niveau des enceintes (Level Calibration)
Ajuste le volume relatif de chaque enceinte pour un équilibre parfait :

```powershell
Setup → 2. Speaker → 4. Level Calibration
```

- Plage : `-12.0 dB` à `+12.0 dB` (par pas de 0.5 dB)
- Une tonalité de test est émise à chaque ajustement pour validation à l'oreille [p.134]

### Réglages THX Audio (si applicable)
Si tu utilises des enceintes certifiées THX :

| Paramètre | Réglage recommandé | Effet |
|-----------|-------------------|-------|
| Back Speaker Spacing | `>4.0 ft / >1.2 m` | Optimise le champ surround arrière [p.136] |
| THX Ultra/Select Subwoofer | `Yes` (si caisson THX) | Active le traitement THX pour le LFE |
| BGC (Boundary Gain Compensation) | `On` (si enceintes près d'un mur) | Compense l'accentuation des basses près des murs |
| Loudness Plus | `On` | Maintient la dynamique à bas volume [p.136, p.197] |

### Speaker Virtualizer
Active/désactive les modes d'écoute virtuels (ex: `T-D Theater-Dimensional`) qui simulent un champ surround avec peu d'enceintes :

```powershell
Setup → 2. Speaker → 8. Speaker Virtualizer → On/Off
```

> ⚠️ Désactivé, les modes virtuels comme `T-D` ne seront pas disponibles [p.137, p.196].

---

## 🔧 Dépannage rapide : Calibration

| Problème | Cause probable | Solution |
|----------|---------------|----------|
| "Noise Error" pendant AccuEQ | Micro mal branché ou bruit ambiant | Vérifie le branchement du micro, réduis les bruits [p.181] |
| Distances incohérentes après calibration | Enceintes mal positionnées ou réflexions fortes | Répète la mesure avec un micro bien placé [p.134, p.181] |
| Pas de son après Dirac Live | Profil non transféré ou mode d'écoute incompatible | Vérifie que le profil est bien sélectionné dans `Room EQ → Dirac Live` [p.93, p.166] |
| Basses trop présentes | Double Bass activé + enceintes "Small" | Désactive `Double Bass` ou règle les avant sur "Full Band" [p.133] |

---

[⬅️ Retour au README](../../README.md) | [⏭️ Suite : Modes d'écoute](./modes_ecoute.md)

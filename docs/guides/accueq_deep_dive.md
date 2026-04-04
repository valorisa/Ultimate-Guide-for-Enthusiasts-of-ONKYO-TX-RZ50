# 🎧 AccuEQ Deep Dive - Guide avancé

> 📋 Comparaison AccuEQ vs Dirac Live, réglages avancés, et optimisation
> Basé sur les pages 124-143 du manuel officiel Onkyo TX-RZ50

## 🟢 Pour les débutants : AccuEQ vs Dirac Live, lequel choisir ?

Le TX-RZ50 propose **deux systèmes de calibration** :

| Système | Technologie | Inclus | Correction |
|---------|------------|--------|------------|
| **AccuEQ** | EQ paramétrique + délai | ✅ Gratuit | Fréquence + distance |
| **Dirac Live** | Correction temporelle + fréquentielle | 💳 Licence payante | Fréquence + phase + temps |

### Quand utiliser AccuEQ ?

- ✅ Pièce petite à moyenne (< 25 m²)
- ✅ Enceintes de qualité correcte
- ✅ Budget limité (gratuit)
- ✅ Configuration simple (5.1 ou 7.1)

### Quand utiliser Dirac Live ?

- ✅ Pièce moyenne à grande (> 25 m²)
- ✅ Problèmes acoustiques importants (résonances, écho)
- ✅ Double subwoofer
- ✅ Calibration multi-position (9 points)
- ✅ Correction de phase précise

> 📌 **Note** : Vous pouvez utiliser AccuEQ **avant** Dirac Live pour un pré-réglage, mais Dirac Live écrasera les réglages AccuEQ.

---

## 🔵 Pour les experts : AccuEQ en détail

### Types de mesure AccuEQ

| Mode | Points de mesure | Usage |
|------|-----------------|-------|
| `Full Auto MCACC` | 1 position (principale) | Configuration rapide |
| `Custom` | 1-3 positions | Écoute multi-zone |
| `Professional` | 3-6 positions | Calibration avancée |

### Procédure de mesure AccuEQ

```text
Setup → 2. Speaker → AccuEQ Setup → Start
```

1. **Brancher le micro** AccuEQ fourni sur la prise `SETUP MIC` (façade avant) [p.125]
2. **Placer le micro** à hauteur d'oreille, pointe vers le plafond [p.126]
3. **Silence total** dans la pièce pendant la mesure (~3 min)
4. **Vérifier les résultats** : distances, niveaux, crossover

### Paramètres ajustables après calibration

| Paramètre | Plage | Recommandé | Référence |
|-----------|-------|------------|-----------|
| `Speaker Distance` | 0.30 - 15.00 m | Valeur mesurée par AccuEQ | [p.128] |
| `Speaker Level` | -12 dB à +12 dB | Ajustement fin ±2 dB max | [p.129] |
| `Crossover` | 30-250 Hz | 80 Hz (THX) | [p.130] |
| `Speaker Size` | Large / Small | Small si crossover < 150 Hz | [p.127] |
| `Subwoofer Mode` | Plus / LFE | LFE pour double sub | [p.131] |

### Optimisation manuelle post-AccuEQ

#### 1. Ajustement des niveaux

```text
Après AccuEQ, les niveaux peuvent être ajustés manuellement :
Setup → 2. Speaker → Manual Speaker Setup → Level
```

| Enceinte | Ajustement typique | Pourquoi |
|----------|-------------------|----------|
| Centrale | +1 à +2 dB | Améliore la intelligibilité des dialogues |
| Surround | -1 à -2 dB | Évite un son trop présent derrière |
| Height | 0 dB | Laisser la calibration AccuEQ décider |
| Subwoofer | +2 à +4 dB | Compense la réponse des petites pièces |

#### 2. Réglage du crossover

```text
Setup → 2. Speaker → Manual Speaker Setup → Crossover
```

| Configuration | Crossover recommandé |
|--------------|---------------------|
| Enceintes tower (full range) | 40-60 Hz |
| Enceintes bookshelf | 80 Hz |
| Enceintes satellite | 100-120 Hz |
| Mélange de tailles | 80 Hz (pour toutes) |

> 📌 **Règle THX** : 80 Hz est le standard pour une transition fluide entre satellites et subwoofer.

#### 3. AccuEQ All-Channel Adjust

```text
Setup → 2. Speaker → AccuEQ Setup → AccuEQ All Channel Adjust
```

| Mode | Description | Usage |
|------|------------|-------|
| `On` | Correction sur toutes les enceintes | Par défaut, recommandé |
| `Off` | Correction uniquement sur les frontales | Si vous préférez le son naturel des surrounds |
| `Front Only` | Correction uniquement sur les avant | Pour les puristes stéréo |

---

## 📊 AccuEQ vs Dirac Live : Comparaison technique

| Critère | AccuEQ | Dirac Live |
|---------|--------|------------|
| **Correction fréquentielle** | ✅ EQ paramétrique (19 bandes) | ✅ FIR filters (résolution illimitée) |
| **Correction temporelle** | ❌ Délais uniquement | ✅ Correction de phase complète |
| **Correction impulse response** | ❌ | ✅ |
| **Points de mesure** | 1-6 | 9-25 |
| **Cibles personnalisables** | ❌ Courbe fixe | ✅ Courbe cible libre |
| **Correction subwoofer** | ✅ Basique | ✅ Avancée (Bass Control) |
| **Multi-sub** | ❌ | ✅ |
| **Temps de mesure** | ~3 min | ~15 min |
| **Prix** | Gratuit | Licence payante |

### Résultats de mesure typiques

#### Avant calibration
```text
Réponse en fréquence : ±12 dB (20 Hz - 20 kHz)
Décay waterfall : 400-600 ms sous 200 Hz
Phase : incohérente entre enceintes
```

#### Après AccuEQ
```text
Réponse en fréquence : ±6 dB (20 Hz - 20 kHz)
Décay waterfall : 300-500 ms sous 200 Hz (inchangé)
Phase : améliorée (délais corrigés)
```

#### Après Dirac Live
```text
Réponse en fréquence : ±3 dB (20 Hz - 20 kHz)
Décay waterfall : 150-250 ms sous 200 Hz
Phase : cohérente entre toutes les enceintes
```

---

## 🔧 Dépannage : AccuEQ

| Problème | Cause probable | Solution |
|----------|---------------|----------|
| `Microphone Error` | Micro non branché | Brancher sur `SETUP MIC` (façade avant) [p.125] |
| `Noise Error` | Bruit ambiant | Fermer fenêtres, couper clim [p.126] |
| `Speaker Not Detected` | Enceinte débranchée | Vérifier câblage, impédance [p.127] |
| `Subwoofer Not Detected` | Sub non alimenté | Vérifier câble LFE, alimentation sub |
| Résultats incohérents | Micro mal positionné | Micro hauteur oreille, pointe vers plafond [p.126] |
| Basses excessives après calibration | Room gain non compensé | Réduire le niveau sub de -3 dB manuellement |

---

## 🔗 Liens utiles

- [Configuration & Calibration](./configuration.md) - AccuEQ, Dirac Live, réglages audio
- [REW + Dirac Live](./rew_dirac.md) - Calibration avancée avec REW
- [Modes d'écoute](./modes_ecoute.md) - Dolby Atmos, DTS:X, THX
- [Dépannage](./depannage.md) - Codes d'erreur

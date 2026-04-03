# 🎧 Modes d'écoute

> 📋 Basé sur le manuel officiel Onkyo TX-RZ50 [p.89-90, p.183-198]

## 🟢 Pour les débutants : Comprendre les catégories de modes

Le TX-RZ50 propose trois catégories de modes d'écoute, accessibles via les touches **MOVIE/TV**, **MUSIC** et **GAME** de la télécommande ou du panneau frontal [p.89].

### Comment sélectionner un mode ?
1. Appuie sur **MOVIE/TV**, **MUSIC** ou **GAME** selon le type de contenu.
2. Tourne la molette **LISTENING MODE** pour parcourir les modes disponibles dans cette catégorie.
3. Le mode sélectionné s'affiche sur l'écran principal et le téléviseur [p.90].

> 💡 **Astuce** : Chaque touche mémorise le dernier mode utilisé. Si le contenu est incompatible, le TX-RZ50 bascule automatiquement sur le mode le plus adapté.

### Catégories simplifiées
| Touche | Usage recommandé | Exemples de modes |
|--------|-----------------|------------------|
| 🎬 **MOVIE/TV** | Films, séries, émissions TV | Dolby Atmos, DTS:X, THX Cinema |
| 🎵 **MUSIC** | Musique, concerts, podcasts | Stereo, Direct, Pure Audio, Orchestra |
| 🎮 **GAME** | Jeux vidéo, gaming immersif | Game-Action, Game-RPG, Game-Sports |

---

## 🔵 Pour les experts : Détails techniques des modes

### Modes Dolby & DTS (immersion cinéma)

#### 🎬 Dolby Atmos
- **Principe** : Audio objet-based (positionnement 3D précis des sons)
- **Configuration requise** : Enceintes en hauteur (Height/Top) ou Dolby Enabled [p.192]
- **Modes affichés selon la config** :
  - `Atmos 2.0/2.1` : Enceintes avant uniquement
  - `Atmos 5.1/7.1` : Système surround complet
  - `Atmos` : Config avec enceintes en hauteur (5.1.2, 7.1.4, etc.)
- **Activation** : Source Dolby Atmos + câble HDMI + sortie Bitstream sur le lecteur [p.192]

#### 🎬 DTS:X
- **Principe** : Alternative à Atmos, également objet-based
- **Compatibilité** : Mêmes configurations que Dolby Atmos [p.194]
- **Mode DTS Neural:X** : Upscale les sources 5.1 vers 7.1.2/5.1.4 pour une immersion accrue [p.194]

#### 🎬 IMAX Enhanced
- **Principe** : Contenu remasterisé avec traitement DTS:X + calibration IMAX
- **Modes** :
  - `IMAX DTS` : Contenu 5.1 remasterisé
  - `IMAX DTS:X` : Contenu objet-based immersif
  - `IMAX Neural:X` : Upscale des sources IMAX 5.1 vers configs avancées [p.195]
- **Activation** : `IMAX Mode` = `Auto` (défaut) ou `On` si non détecté [p.139]

### Modes THX (certification professionnelle)

| Mode | Usage | Caractéristiques techniques |
|------|-------|----------------------------|
| **THX Cinema** | Films en home-cinéma | Re-EQ, Timbre Matching, Adaptive Decorrelation, Loudness Plus [p.197] |
| **THX Select Cinema** | Pièces < 20 m³ | ASA (Advanced Speaker Array) pour transition surround fluide [p.198] |
| **THX Music** | Musique mastérisée | Timbre Matching + Loudness Plus adapté au niveau musical [p.197] |
| **THX Games** | Jeux immersifs | Spatialisation précise + Loudness Plus niveau jeu [p.197] |

> ⚠️ **Note THX** : Les modes THX désactivent les calibrations Dirac Live [p.197].

### Modes Musique (fidélité audio)

| Mode | Description | Quand l'utiliser |
|------|-------------|-----------------|
| **Stereo** | Son stéréo sur enceintes avant + sub | Écoute musicale classique, podcasts |
| **Direct** | Signal brut, traitement minimal | Audiophiles souhaitant un son "pur" [p.193] |
| **Pure Audio** | Circuit vidéo désactivé, audio ultra-pur | Écoute critique, pas de vidéo nécessaire [p.196] |
| **Orchestra** | Champ sonore élargi, réverbération simulée | Musique classique, opéra, jazz acoustique [p.196] |
| **Unplugged** | Champ avant accentué, scène virtuelle | Concerts acoustiques, voix solo [p.198] |
| **Studio-Mix** | Image acoustique puissante, ambiance club | Pop, rock, électro [p.196] |
| **AllCh Stereo** | Même signal stéréo sur toutes les enceintes | Musique d'ambiance, pièces larges [p.192] |

### Modes Jeu (optimisation gaming)

| Mode | Usage | Effet principal |
|------|-------|----------------|
| **Game-Action** | Jeux d'action, FPS | Spatialisation précise des effets (pas, tirs) |
| **Game-RPG** | Jeux de rôle, aventures | Ambiance immersive, dialogues clairs |
| **Game-Rock** | Jeux rythmiques, musique | Basses renforcées, dynamique élevée |
| **Game-Sports** | Jeux de sport, courses | Ambiance stade, commentaires avant [p.195] |

> ⚠️ **Note Gaming** : Les modes Game désactivent Dirac Live pour réduire la latence [p.195].

### Modes virtuels (Speaker Virtualizer)

Lorsque `Speaker Virtualizer` = `On` (défaut) [p.137], ces modes créent un champ surround virtuel avec peu d'enceintes :

| Mode | Config minimale | Effet |
|------|----------------|-------|
| **T-D (Theater-Dimensional)** | 2.1 ou 3.1 | Surround virtuel à partir de 2-3 enceintes [p.196] |
| **TV Logic** | 2.1 | Dialogues renforcés, ambiance studio TV [p.198] |
| **Mono Music** | 1.1 | Même son mono sur toutes les enceintes (accessibilité) [p.196] |

> ⚠️ **Désactivation** : Si `Speaker Virtualizer` = `Off`, les modes T-D, TV Logic ne sont plus disponibles [p.196].

---

## 📊 Tableaux de compatibilité

### Formats d'entrée → Modes disponibles

| Format d'entrée | Modes compatibles | Notes |
|----------------|-----------------|-------|
| **Dolby Digital (DD)** | DD, Atmos*, DSur*, Stereo, Direct | *Si config enceintes compatible [p.188] |
| **Dolby Atmos** | Atmos, DSur, Stereo, Direct | Nécessite HDMI + Bitstream [p.192] |
| **DTS** | DTS, DTS:X*, Neural:X*, Stereo | *Si config + source compatible [p.194] |
| **DTS:X** | DTS:X, Neural:X, Stereo, Direct | HDMI + Bitstream requis [p.194] |
| **PCM 2ch** | Tous les modes | Format universel [p.188] |
| **DSD** | DSD, Stereo, Direct, Pure Audio | Fréq. ≤ 11.2 MHz [p.193] |
| **IMAX Enhanced** | IMAX DTS, IMAX DTS:X, Neural:X | Contenu spécifique requis [p.195] |

### Configurations d'enceintes → Modes disponibles

| Config | Modes Atmos | Modes DTS:X | Modes THX | Modes Virtuels |
|--------|-------------|-------------|-----------|---------------|
| **2.1 / 3.1** | Atmos 2.0/2.1 | ❌ | ❌ | T-D, TV Logic ✅ |
| **5.1** | Atmos 5.1 | DTS:X ✅ | THX Cinema ✅ | ❌ |
| **5.1.2** | Atmos ✅ | DTS:X ✅ | THX Cinema ✅ | ❌ |
| **7.1.4** | Atmos ✅ | DTS:X ✅ | THX Cinema ✅ | ❌ |

> 📌 **Règle générale** : Plus la config est avancée, plus les modes immersifs sont disponibles. Voir tableau complet p.183-185 du manuel.

---

## 🔧 Dépannage rapide : Modes d'écoute

| Problème | Cause probable | Solution |
|----------|---------------|----------|
| Mode désiré grisé/non disponible | Config enceintes incompatible | Vérifier `Speaker Channels` dans Setup → Speaker [p.131] |
| Pas de son Atmos/DTS:X | Source non Bitstream ou câble HDMI inadéquat | Régler lecteur sur Bitstream + câble High Speed [p.192] |
| Mode Pure Audio impossible | Multizone activée ou casque branché | Désactiver Multizone / débrancher casque [p.196] |
| Modes virtuels indisponibles | `Speaker Virtualizer` = Off | Activer dans Setup → Speaker → Speaker Virtualizer [p.137] |
| Son Atmos mais pas d'effets hauteur | Enceintes Height mal configurées | Vérifier `Height 1/2 Speaker` dans Initial Setup [p.159] |

---

[⬅️ Retour au README](../../README.md) | [⏭️ Suite : Dépannage](./depannage.md)

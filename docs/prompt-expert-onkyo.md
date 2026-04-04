<role>
Tu es un Expert Technique en Audio-Vidéo, Ingénieur Documentation Open Source et Architecte Logiciel.
</role>

<contexte>
Tu disposeras du texte intégral du mode d'emploi du récepteur AV Onkyo TX-RZ50. Ton objectif est double : 
1. Produire une explicitation technique exhaustive ET pédagogique du document.
2. Concevoir l'architecture complète d'un dépôt GitHub prêt à l'emploi, incluant documentation auto-générée (Sphinx), scripts Python fonctionnels et conteneurisation Docker.
</contexte>

<contraintes>
- Langue : Français technique précis, pédagogique et sans fioritures.
- Format : Markdown strict, titres hiérarchiques, tableaux, listes, blocs de code.
- Exactitude : Strictement ancrée au texte fourni. Aucune spéculation. Signale les ambiguïtés ou infos manquantes avec `[⚠️ À vérifier p.X]`.
- Références : Cite systématiquement la page ou section entre crochets `[p.X]` pour chaque donnée technique, spécification ou procédure.
- Public : Dualité obligatoire dans chaque section technique :
  • 🟢 "Pour les débutants" : explication simplifiée, analogies, checklist pas-à-pas.
  • 🔵 "Pour les experts" : spécifications brutes, limites, pièges de configuration, optimisations avancées.
- Segmentation : Génère la réponse en DEUX BLOCS SÉQUENTIELS. Attends une validation explicite entre les blocs.
</contraintes>

<taches_phase_1>
PHASE 1 — EXPLICITATION TECHNIQUE PÉDAGOGIQUE :
1. Décompose le manuel en modules logiques : Installation & Sécurité, Raccordements (HDMI/eARC, analogique/numérique, antennes), Configuration & Calibration (Dirac Live, AccuEQ), Modes d'écoute & Formats (Dolby, DTS, THX, IMAX), Multizone (ZONE 2/3/B), Connectivité (Réseau, Bluetooth, Streaming, Home Automation via RS-232/HTTP), Dépannage & Codes d'erreur.
2. Pour chaque module : applique la structure 🟢/🔵, extrais les procédures critiques, pièges courants et limites techniques.
3. Génère 3 tableaux de référence rapides avec citations `[p.X]` :
   a) Compatibilité Modes d'écoute × Formats d'entrée
   b) Combinaisons d'enceintes × Bornes utilisées × Limites Multizone
   c) Codes d'erreur × Causes probables × Résolutions
4. Ajoute en fin de phase : "FAQ Débutant" (10 questions fréquentes) et "Cheat Sheet Expert" (raccourcis, limites cachées, optimisations RS-232/HTTP).
</taches_phase_1>

<taches_phase_2>
PHASE 2 — ARCHITECTURE GITHUB & SCRIPTS (Stack Python/Sphinx/Docker) :
1. Fournis une arborescence complète au format `tree` :
   /docs/source/          (Sphinx .rst/.md files)
   /scripts/              (Python uniquement)
   /docker/               (Dockerfile, docker-compose.yml, .dockerignore)
   /config/               (Home Assistant YAML, Postman/HTTP collections)
   .github/ISSUE_TEMPLATE/
   README.md, LICENSE, ATTRIBUTION.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, requirements.txt, requirements-docs.txt, Makefile (Sphinx)

2. Contenu obligatoire des fichiers clés :
   • README.md : Badges, description, TOC, Quickstart (5 min), liens officiels, guide d'installation Docker, structure du projet.
   • LICENSE : Texte standard MIT.
   • ATTRIBUTION.md : Clause d'attribution explicite à Onkyo Home Entertainment Corp. pour les extraits du manuel, précisant l'usage éducatif/fair use et la distinction code vs contenu protégé.
   • docs/conf.py & docs/index.rst : Configuration Sphinx complète prête à générer la doc (thème sphinx-rtd-theme, extensions autodoc, napoleon pour docstrings Google).
   • requirements-docs.txt : sphinx, sphinx-rtd-theme, myst-parser.

3. Scripts Python fonctionnels (`/scripts/`) avec docstrings Sphinx & exemples :
   • rs232_control.py : Wrapper `pyserial` (allumage, sélection source, volume, retour d'état) avec gestion timeouts et reconnexion.
   • http_api_wrapper.py : Wrapper `requests` pour l'API Web Setup du TX-RZ50 (GET/POST endpoints réseau, authentification admin par défaut, parsing JSON).
   • log_parser.py : Analyseur de logs/retours série et HTTP, détection automatique des codes d'erreur, export CSV/JSON.
   • firmware_checker.py : Vérification version firmware via réseau, comparaison avec version locale, notification de mise à jour.
   Chaque script doit inclure : `__doc__` formatée Sphinx, `argparse` CLI, gestion d'erreurs `try/except`, logging structuré, et bloc `if __name__ == "__main__":`.

4. Docker & Déploiement :
   • Dockerfile : Image Python 3.11-slim, utilisateur non-root, copie des scripts, installation deps, ENTRYPOINT configurable, HEALTHCHECK.
   • docker-compose.yml : Services `onkyo-control` (scripts), `onkyo-docs` (serveur Sphinx auto-reload), volumes persistants pour `/config` et `/logs`.
   • .dockerignore : exclusion venv, .git, __pycache__, manuels.

5. Recommandations CI/CD : GitHub Actions pour lint Python (ruff/black), validation Sphinx (`make html`), build Docker, et publication auto sur GitHub Pages.
</taches_phase_2>

<output_instructions>
- Commence immédiatement par : `## 📚 PHASE 1 : EXPLICITATION TECHNIQUE PÉDAGOGIQUE`
- Après la Phase 1, insère exactement : `--- ✋ PAUSE : Réponds "CONTINUER PHASE 2" pour générer l'architecture GitHub complète.`
- N'attends pas ma réponse pour générer, mais structure ton output pour que je puisse interrompre si besoin. (Optionnel : si le contexte est saturé, scinde en 2 messages).
- Ne génère aucun texte d'introduction, de conclusion ou de métadonnées hors des balises et consignes.
</output_instructions>

<input>
[COLLER LE TEXTE COMPLET DU PDF ICI] (le PDF sera fourni en pièce-jointe car sa taille est de 18.3 Mo)
</input>
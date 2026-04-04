# Guide de Contribution

Merci de contribuer à **Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50** ! 🎉

## 🚀 Démarrage rapide

```bash
# 1. Fork le dépôt et clonez-le
git clone https://github.com/VOTRE_USERNAME/Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50.git
cd Ultimate-Guide-for-Enthusiasts-of-ONKYO-TX-RZ50

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# 3. Installer les dépendances
pip install -r scripts/requirements.txt
pip install -r requirements-docs.txt

# 4. Créer une branche
git checkout -b feat/ma-fonctionnalite
```

## 📋 Standards de code

### Python
- **Style** : PEP 8, vérifié par `ruff` et `black`
- **Docstrings** : Format Sphinx pour la génération auto de la documentation
- **Typing** : Utiliser les annotations de type modernes (`str | None` au lieu de `Optional[str]`)
- **Tests** : Chaque nouveau script doit avoir des tests unitaires (`pytest`)

```bash
# Vérifier le lint
make lint

# Formater le code
make lint-fix

# Lancer les tests
make test
```

### Documentation
- **Guides** : Markdown dans `docs/guides/`
- **Sphinx** : Fichiers `.rst` dans `docs/source/` avec `.. include:: ../guides/*.md`
- **Références** : Citer les pages du manuel officiel entre crochets `[p.X]`
- **Langue** : Français par défaut, traduction EN bienvenue

### Git
- **Commits** : Messages clairs et descriptifs (format conventionnel recommandé)
- **Branches** : `feat/`, `fix/`, `docs/`, `chore/`
- **PR** : Description claire, screenshots si applicable, tests passants

## 🔍 Processus de review

1. Ouvrir une **Pull Request** vers `dev`
2. Le **CI** doit passer (lint + tests + docs)
3. Un **mainteneur** review le code
4. Après approbation, **merge** dans `dev`
5. **Merge `dev` → `main`** pour le déploiement

## 📁 Structure du projet

```
├── docs/
│   ├── guides/          # Documentation Markdown (contenu)
│   └── source/          # Fichiers Sphinx (.rst)
├── scripts/
│   ├── tests/           # Tests unitaires
│   └── *.py             # Scripts Python
├── config/              # Fichiers de configuration (HA, Node-RED)
├── custom_component/    # Custom Component Home Assistant
└── docker/              # Configuration Docker
```

## 🐛 Rapport de bug

Utilisez le template [bug_report.md](.github/ISSUE_TEMPLATE/bug_report.md) avec :
- La version du firmware du TX-RZ50
- Les logs pertinents
- Les étapes pour reproduire le problème

## 💡 Suggestions

Pour les suggestions de documentation, utilisez le template [doc_suggestion.md](.github/ISSUE_TEMPLATE/doc_suggestion.md).

## 📜 Licence

En contribuant, vous acceptez que vos contributions soient distribuées sous la licence **MIT** de ce projet.

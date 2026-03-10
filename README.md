# GrabYT

<p align="center">
  <img src="assets/favicon.svg" alt="GrabYT" width="96" height="96"/>
</p>

Application de bureau pour télécharger des vidéos ou audios depuis YouTube à partir d’un fichier d’URLs. Interface PyQt6 (fenêtres sans bordure, thème pastel), moteur yt-dlp.

---

## Fonctionnalités

- **Fichier d’URLs** : un fichier texte (par défaut `urls.txt`) contenant une URL YouTube par ligne ; les lignes commençant par `#` sont ignorées. Choix du fichier et ouverture dans l’éditeur par défaut depuis l’interface.
- **Validation** : avant téléchargement, initialisation qui vérifie les liens et affiche le nombre total, valides et invalides, avec une barre de progression pendant l’analyse.
- **Téléchargement** : lancement en un clic après validation ; progression détaillée (piste en cours, pourcentage, ETA) dans une fenêtre dédiée ; annulation possible.
- **Historique** : fenêtre listant les téléchargements passés (depuis `download.json`) avec accès rapide au lien YouTube de chaque entrée.
- **Interface** : barre de titre personnalisée (déplacement, minimiser/restaurer/fermer), icône d’application depuis `assets/favicon.svg`, tooltips arrondis pour les boutons circulaires, thème cohérent sur toutes les fenêtres.

---

## Utilisation

1. **Lancer l’application**  
   Exécutable : `dist\GrabYT-full.exe` ou `dist\GrabYT-slim.exe` selon le build. En développement : `python main.py`.

2. **Choisir le fichier d’URLs**  
   Le champ indique le fichier utilisé (par défaut `urls.txt` à la racine). Utilisez « Parcourir » pour en sélectionner un autre. Le bouton circulaire à droite permet d’ouvrir le fichier dans l’éditeur par défaut.

3. **Initialiser**  
   Cliquer sur « Initialiser (nombre de musiques, liens valides / non valides) ». La validation des URLs s’effectue et une barre de progression affiche l’avancement. À la fin, les statistiques (total, valides, invalides) s’affichent et le même bouton devient « Démarrer le téléchargement ».

4. **Démarrer le téléchargement**  
   Cliquer sur « Démarrer le téléchargement ». Une fenêtre de progression s’ouvre (piste en cours, pourcentage, ETA). À la fin, un bouton permet d’ouvrir le dossier des téléchargements.

5. **Historique**  
   Le bouton circulaire « Historique » (à droite du bouton d’action) ouvre la liste des téléchargements passés. Un clic sur une carte ouvre le lien YouTube associé.

**Prérequis (build slim uniquement)** : ffmpeg doit être installé et accessible dans le PATH. Le build « full » inclut ffmpeg (imageio-ffmpeg) et ne nécessite aucune installation supplémentaire.

---

## Configuration

Le fichier `config/config.yaml` permet de modifier :

| Clé | Description | Défaut |
|-----|-------------|--------|
| `app_name` | Titre affiché dans la fenêtre principale | `GRABYT` |
| `default_urls_file` | Fichier d’URLs par défaut | `urls.txt` |
| `downloads_dir` | Dossier de destination des téléchargements | `downloads` |
| `max_concurrent_downloads` | Nombre de téléchargements simultanés | `3` |

Les chemins peuvent être relatifs (à la racine du projet ou au répertoire de l’exécutable) ou absolus.

---

## Build

Génération des exécutables Windows dans `dist\` :

```bash
build.bat [--build full|slim]
```

| Option | Description |
|--------|-------------|
| `--build full` (défaut) | Exe **portable** : inclut imageio-ffmpeg. Plus lourd, aucune installation de ffmpeg requise. Produit `dist\GrabYT-full.exe`. |
| `--build slim` | Exe **léger** : sans ffmpeg inclus. ffmpeg doit être installé sur la machine cible. Produit `dist\GrabYT-slim.exe`. |

**Prérequis** : environnement virtuel activé, PyInstaller installé (`pip install pyinstaller`). Le script appelle `scripts/build_icon.py` pour générer `assets/icon.ico` à partir de `assets/favicon.svg` ; si `icon.ico` est absent, l’exe est produit sans icône système. L’application utilise en priorité `assets/favicon.svg` pour l’icône affichée dans l’interface (fenêtres et barre de titre).

---

## Structure du projet

```
grabyt/
  main.py                 # Point d'entrée
  config/config.yaml      # Configuration
  assets/
    favicon.svg           # Icône application (prioritaire)
    icon.ico              # Icône exe (générée par build_icon.py)
  src/
    config_loader.py      # Chargement de la config
    core/
      download_manager.py # Gestion des téléchargements et historique
      downloader.py       # Intégration yt-dlp
      url_parser.py       # Parsing du fichier URLs
      url_validator.py    # Validation des liens
    ui/
      main_window.py      # Fenêtre principale
      progress_window.py  # Fenêtre de progression
      history_window.py   # Fenêtre historique
      title_bar.py        # Barre de titre personnalisée
      icons.py            # Icônes (favicon.svg, icon.ico, SVG internes)
      rounded_tooltip.py  # Tooltips arrondis
      styles.py           # Feuilles de style
  scripts/
    build_icon.py         # Génération de icon.ico depuis favicon.svg
  build_full.spec         # Spec PyInstaller (full)
  build_slim.spec         # Spec PyInstaller (slim)
  build.bat               # Script de build Windows
```

---

## Licence

Ce projet est distribué sous la **licence Apache 2.0**. En résumé :

- **Utilisation, modification et distribution** : vous pouvez utiliser le logiciel, le modifier et le redistribuer (y compris à titre commercial), sous réserve de conserver une copie de la licence et les mentions de copyright.
- **Attribution** : les redistributions (code source ou binaire) doivent indiquer les changements éventuels et inclure le texte de la licence. Il n’est pas obligatoire de mentionner Apache dans une interface utilisateur.
- **Brevets** : les contributeurs accordent une licence d’utilisation des brevets qu’ils détiennent sur les apports qu’ils ont fournis.
- **Sans garantie** : le logiciel est fourni « tel quel », sans garantie d’aucune sorte.

Le texte complet est dans le fichier [LICENSE](LICENSE).

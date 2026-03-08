# GrabYT

<p align="center">
  <img src="assets/icon.ico" alt="GrabYT" width="96" height="96"/>
</p>

Application de bureau pour télécharger des vidéos ou audios depuis YouTube à partir d’un fichier d’URLs. Interface PyQt6, moteur yt-dlp.

---

## Utilisation

1. **Lancer l’application**  
   Double-cliquer sur `GrabYT.exe` (ou exécuter avec Python : `python main.py`).

2. **Fichier d’URLs**  
   Par défaut le logiciel utilise `urls.txt` à la racine. Une URL par ligne (YouTube, etc.). Vous pouvez choisir un autre fichier via l’interface.

3. **Dossier de téléchargement**  
   Indiquer le dossier de destination (par défaut : `downloads`). Les médias y sont enregistrés.

4. **Lancer le téléchargement**  
   Cliquer sur le bouton de démarrage. La progression s’affiche ; vous pouvez annuler en cours de route.

**Prérequis (version slim uniquement)** : si vous utilisez l’exécutable « slim », ffmpeg doit être installé et accessible dans le PATH du système.

---

## Build

Génération de l’exécutable Windows dans `dist\` :

```bash
build.bat [--build full|slim]
```

| Option | Description |
|--------|-------------|
| `--build full` (défaut) | Exe **portable** : inclut imageio-ffmpeg. Plus lourd, aucune installation de ffmpeg requise. |
| `--build slim` | Exe **léger** : sans ffmpeg inclus. ffmpeg doit être installé sur la machine cible. |

Environnement recommandé : venv activé, PyInstaller installé (`pip install pyinstaller`). L’icône est générée automatiquement avant le build via `scripts/build_icon.py` ; si `assets/icon.ico` est absent, l’exe sera produit sans icône.

Résultat : `dist\GrabYT.exe`.

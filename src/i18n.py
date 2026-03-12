# Internationalisation: traductions FR/EN/DE/ES, langue selectionnable via config.

from typing import Any

# Traductions: cle -> { "fr": "...", "en": "...", "de": "...", "es": "..." }
_TRANSLATIONS: dict[str, dict[str, str]] = {
    "file_group_title": {
        "fr": "Fichier de liens",
        "en": "URL file",
        "de": "Link-Datei",
        "es": "Archivo de enlaces",
    },
    "file_placeholder": {
        "fr": "Chemin vers le fichier URLs...",
        "en": "Path to URL file...",
        "de": "Pfad zur URL-Datei...",
        "es": "Ruta del archivo de URLs...",
    },
    "browse": {"fr": "Parcourir", "en": "Browse", "de": "Durchsuchen", "es": "Examinar"},
    "browse_dialog_title": {
        "fr": "Choisir le fichier de liens",
        "en": "Choose URL file",
        "de": "Link-Datei auswählen",
        "es": "Elegir archivo de enlaces",
    },
    "init_group_title": {
        "fr": "Initialisation",
        "en": "Initialization",
        "de": "Initialisierung",
        "es": "Inicialización",
    },
    "init_button": {
        "fr": "Initialiser (nombre de musiques, liens valides / non valides)",
        "en": "Initialize (count, valid / invalid links)",
        "de": "Initialisieren (Anzahl, gültige / ungültige Links)",
        "es": "Inicializar (cantidad, enlaces válidos / no válidos)",
    },
    "start_button": {
        "fr": "Demarrer le telechargement",
        "en": "Start download",
        "de": "Download starten",
        "es": "Iniciar descarga",
    },
    "downloading": {
        "fr": "Telechargement en cours...",
        "en": "Downloading...",
        "de": "Download läuft...",
        "es": "Descargando...",
    },
    "stats_none": {
        "fr": "Aucune initialisation effectuee.",
        "en": "No initialization done.",
        "de": "Keine Initialisierung durchgeführt.",
        "es": "No se ha realizado ninguna inicialización.",
    },
    "stats_select_file": {
        "fr": "Veuillez selectionner un fichier.",
        "en": "Please select a file.",
        "de": "Bitte wählen Sie eine Datei.",
        "es": "Seleccione un archivo.",
    },
    "stats_file_missing": {
        "fr": "Le fichier specifie n'existe pas.",
        "en": "The specified file does not exist.",
        "de": "Die angegebene Datei existiert nicht.",
        "es": "El archivo especificado no existe.",
    },
    "stats_no_urls": {
        "fr": "Aucune URL YouTube trouvee dans le fichier.",
        "en": "No YouTube URL found in the file.",
        "de": "Keine YouTube-URL in der Datei gefunden.",
        "es": "No se encontró ninguna URL de YouTube en el archivo.",
    },
    "stats_file_changed": {
        "fr": "Fichier modifie. Reinitialiser pour mettre a jour les statistiques.",
        "en": "File changed. Re-initialize to update statistics.",
        "de": "Datei geändert. Erneut initialisieren, um die Statistiken zu aktualisieren.",
        "es": "Archivo modificado. Reinicializar para actualizar las estadísticas.",
    },
    "stats_validation": {
        "fr": "Validation des liens en cours...",
        "en": "Validating links...",
        "de": "Links werden geprüft...",
        "es": "Validando enlaces...",
    },
    "stats_format": {
        "fr": "Total: {total} | Valides: {valid} | Invalides: {invalid}",
        "en": "Total: {total} | Valid: {valid} | Invalid: {invalid}",
        "de": "Gesamt: {total} | Gültig: {valid} | Ungültig: {invalid}",
        "es": "Total: {total} | Válidos: {valid} | No válidos: {invalid}",
    },
    "validation_progress": {
        "fr": "Validation: {current} / {total} liens...",
        "en": "Validation: {current} / {total} links...",
        "de": "Prüfung: {current} / {total} Links...",
        "es": "Validación: {current} / {total} enlaces...",
    },
    "progress_window_title": {
        "fr": "Progression",
        "en": "Progress",
        "de": "Fortschritt",
        "es": "Progreso",
    },
    "process_group": {"fr": "Process", "en": "Process", "de": "Ablauf", "es": "Proceso"},
    "in_progress": {"fr": "En cours", "en": "In progress", "de": "In Bearbeitung", "es": "En curso"},
    "operation_terminee": {
        "fr": "Operation terminee !",
        "en": "Operation completed!",
        "de": "Vorgang abgeschlossen!",
        "es": "Operación completada.",
    },
    "avancement": {"fr": "Avancement", "en": "Progress", "de": "Fortschritt", "es": "Avance"},
    "eta": {"fr": "ETA: {eta}", "en": "ETA: {eta}", "de": "ETA: {eta}", "es": "ETA: {eta}"},
    "eta_none": {"fr": "ETA: --", "en": "ETA: --", "de": "ETA: --", "es": "ETA: --"},
    "vers_musiques": {
        "fr": "Vers les musiques",
        "en": "Open folder",
        "de": "Ordner öffnen",
        "es": "Abrir carpeta",
    },
    "termine": {"fr": "Termine.", "en": "Done.", "de": "Fertig.", "es": "Finalizado."},
    "termine_pct": {
        "fr": "Termine a {pct:.0f}% ({ok}/{total} reussis)",
        "en": "Done at {pct:.0f}% ({ok}/{total} succeeded)",
        "de": "Fertig bei {pct:.0f}% ({ok}/{total} erfolgreich)",
        "es": "Finalizado al {pct:.0f}% ({ok}/{total} correctos)",
    },
    "history_title": {"fr": "Historique", "en": "History", "de": "Verlauf", "es": "Historial"},
    "history_empty": {
        "fr": "Aucun telechargement dans l'historique.",
        "en": "No downloads in history.",
        "de": "Keine Downloads im Verlauf.",
        "es": "No hay descargas en el historial.",
    },
    "tooltip_open_file": {
        "fr": "Ouvrir le fichier dans l'éditeur par défaut",
        "en": "Open file in default editor",
        "de": "Datei im Standard-Editor öffnen",
        "es": "Abrir archivo en el editor predeterminado",
    },
    "tooltip_history": {
        "fr": "Historique des telechargements",
        "en": "Download history",
        "de": "Download-Verlauf",
        "es": "Historial de descargas",
    },
    "new_version": {
        "fr": "Une nouvelle version ({version}) est disponible.",
        "en": "A new version ({version}) is available.",
        "de": "Eine neue Version ({version}) ist verfügbar.",
        "es": "Hay una nueva versión ({version}) disponible.",
    },
    "default_urls_content": {
        "fr": "# Liste d'URLs YouTube (une par ligne).\n# Les lignes commençant par # sont ignorées.\n# Exemple :\n# https://www.youtube.com/watch?v=xxxxx",
        "en": "# List of YouTube URLs (one per line).\n# Lines starting with # are ignored.\n# Example:\n# https://www.youtube.com/watch?v=xxxxx",
        "de": "# Liste von YouTube-URLs (eine pro Zeile).\n# Zeilen mit # am Anfang werden ignoriert.\n# Beispiel:\n# https://www.youtube.com/watch?v=xxxxx",
        "es": "# Lista de URLs de YouTube (una por línea).\n# Las líneas que empiezan por # se ignoran.\n# Ejemplo:\n# https://www.youtube.com/watch?v=xxxxx",
    },
}

_SUPPORTED = ("fr", "en", "de", "es")
_current_lang = "fr"


def set_language(lang: str) -> None:
    """Definit la langue (fr, en, de ou es)."""
    global _current_lang
    _current_lang = lang if lang in _SUPPORTED else "fr"


def t(key: str, **kwargs: Any) -> str:
    """Retourne la traduction pour la cle, avec remplacement optionnel (ex: t('stats_format', total=5, valid=4, invalid=1))."""
    if key not in _TRANSLATIONS:
        return key
    trans = _TRANSLATIONS[key]
    msg = trans.get(_current_lang, trans.get("fr", key))
    if kwargs:
        try:
            msg = msg.format(**kwargs)
        except KeyError:
            pass
    return msg


def get_default_urls_content() -> str:
    """Contenu par defaut du fichier urls.txt (commentaires), selon la langue courante."""
    return t("default_urls_content")

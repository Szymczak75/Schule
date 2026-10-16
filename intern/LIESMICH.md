# Ordner `intern/` – nicht gelistet

Seiten hier erscheinen **nicht** auf der Startseite (`dino_hub.html`), sind aber für jeden
erreichbar, der den Link kennt (z. B. Kollegen). Deshalb hier **nichts Personenbezogenes**.

Jede Seite hier trägt im `<head>`:

    <meta name="robots" content="noindex, nofollow">

damit Suchmaschinen sie nicht aufnehmen.

Wirklich Privates (Entwürfe, Tests, alles mit Namen) gehört in `_privat/` – dieser Ordner
wird durch `.gitignore` nie hochgeladen.

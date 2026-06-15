# Manual screenshots / Capturas del manual

Place the user-manual screenshots here. They are served by Django as static
files and shown inside the in-app manual (`/manual/`).

Coloca aquí las capturas del manual de usuario. Se sirven como ficheros
estáticos y se muestran dentro del manual de la app (`/manual/`).

- Use **exactly** the file names listed in the manual's *Screenshot guide /
  Guía de capturas* (e.g. `05-devices.png`).
- Formato **PNG**, ancho ~**1400 px**, con **datos de ejemplo** (no reales).
- Los manuales están en `../../manuals/` (`MANUAL_USUARIO.md` y `USER_MANUAL.md`).

The in-app manual rewrites the markdown image paths (`images/NN.png`) to
`/static/manual_images/NN.png`, so just dropping the files here is enough.

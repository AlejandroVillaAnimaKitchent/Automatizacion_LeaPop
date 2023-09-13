# Automatización (Super)canales

Aplicación de Streamlit para facilitar la distribución de contenido, especialmente en los supercanales.
  
  
## Tareas pendientes:

- [ ] General
  - [ ] Implementar botones de limpiar selección (que reinicien tanto variables como widgets).
  - [ ] Crear un roadmap/catálogo de nuevas features.

- [ ] Catálogo de vídeos
  - [ ] Añadir Analytics de los vídeos (top views/watchtime en los últimos X días por ejemplo).
  - [ ] Arreglar diferentes versiones de los globos/las pelotas.
  - [ ] Ordenar los vídeos (de momento abc y luego vemos?).
  
- [ ] Catálogo de Miniaturas Canciones/Cuquines
  - [x] Añadir buscador o algo que la haga más útil por su cuenta.
  - [ ] Añadir Analytics a las miniaturas (top minis de los últimos X dias en CTR y clicks o lo que sea).

- [ ] Creador de colecciones aleatorias
  - [x] Que las promos sean aleatorias (Feedback equipo digital).
  - [x] Que el mismo vídeo no esté varias veces seguidas (Feedback equipo digital).
  
- [ ] Editor de colecciones
  - [x] Si da error porque el archivo está abierto que te diga de cerrarlo.
  - [x] Meter un check por si quieren qeue se puedan repetir vídeos (como en colecciones largas/directos).

- [ ] Creador excel de YT
  - [ ] Tags de Oihan para colecciones (está a nivel de código, falta modificar el .csv) y para los canales principales.
  - [x] Dar la opción de subir un archivo de colecciones y/o vídeos creados antes, i.e., sin pasar por Creador de colecciones aleatorias.

  
- [ ] Distribución de contenido
  - [X] Que el sistema que intenta resubir archivos sea más robusto (probablemente falle, pero aún no sabemos como).
  - [ ]  Añadir la opción de usar el archivo creado en la pestaña anterior (Creador excel de YT) o subir un archivo.
  - [ ]  Que pueda ir por API además de por UI.
  
- [ ] Reclamaciones de Copy
  - [X] Que el update_claims_df.py pueda tener en cuenta cuando hay 2 reclamaciones pendientes nuevas. Tener en cuenta que pueden salir 2 pending nuevas a la vez, y alguna pending y otra con la que no se puede interactuar.
  - [ ] Botón para actualizar (y actualización periódica de) las claims. Además, añadir claims desde más allá de la segunda página.
  - [ ] Quitar las de Clan.

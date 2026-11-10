# Poner en marcha la nueva Catequilla (una sola vez)

Todo en la **terminal de Ubuntu**, salvo donde dice PowerShell. Ollama tiene que estar abierto en Windows.

## 1. Configuración de OpenCode (hecho el 10 nov. 2026)

- `presence_penalty` en 0 en `~/.config/opencode/opencode.json`.
- `~/.config/opencode/agents/catequilla.md` con `model: ollama/qwen3.6:27b-coding`.
- `/reload` en OpenCode.

## 2. Compilador de 3DS: Docker (hecho el 10 nov. 2026)

El servidor de devkitPro responde `403` al instalador, así que se usa su imagen oficial de Docker:

```sh
sudo apt install -y build-essential cmake ninja-build python3 zip git wget libsdl2-dev docker.io
sudo usermod -aG docker $USER        # luego, en PowerShell: wsl --shutdown, y abrir Ubuntu otra vez
docker run --rm hello-world          # si no conecta: sudo service docker start
docker pull devkitpro/devkitarm:latest
```

Cada prueba se compila con `platform/3ds/docker-build-test.sh NN`, que hace dentro de Docker lo mismo que `build-test.sh NN`. La primera vez también compila SDL2 (para el PC y para la 3DS) en `build-deps/`: tarda más.

## 3. Fuentes de referencia

```sh
mkdir -p ~/work/refs && cd ~/work/refs
git clone --depth 1 https://github.com/devkitPro/citro3d
git clone --depth 1 https://github.com/devkitPro/libctru
git clone --depth 1 https://github.com/devkitPro/3ds-examples
```

## 4. Los repos

```sh
cd ~/work/3ds-ports
[ -d n3ds-ports ] || git clone https://github.com/AlexanderV387/n3ds-ports
git -C n3ds-ports pull
cd gzdoom-3ds
git fetch origin
git checkout uzdoom-3ds-test25
```

## 5. Las instrucciones nuevas

```sh
cp ~/catequilla/AGENTS.md ~/catequilla/AGENTS.md.antes-10nov
cp ~/work/3ds-ports/n3ds-ports/docs/catequilla/AGENTS.md ~/catequilla/AGENTS.md
opencode service restart
```

## 6. Primera conversación nueva

Abre una conversación **nueva** (no sigas la de "prueba 8"), con el agente Catequilla, y pégale esto:

> Hola Catequilla. Empezamos con instrucciones y herramientas nuevas. Lee ~/catequilla/AGENTS.md y sigue sus pasos de inicio: lee platform/3ds/STATUS.md en ~/work/3ds-ports/gzdoom-3ds (rama uzdoom-3ds-test25), y hechos-3ds.md y plantilla-prueba.md en ~/work/3ds-ports/n3ds-ports/docs/catequilla/. La prueba 25 ya está escrita y su plan está en STATUS.md. Compílala con `platform/3ds/docker-build-test.sh 25` (nada de MSYS2 ni de copiar a C:). Cuando termine, dame la ruta del .3dsx y la hoja de pasadas A, B, C y D. No cambies código.

## 7. Cada prueba siguiente

1. Conversación nueva con Catequilla: "Lee STATUS.md y prepara la prueba NN según la plantilla".
2. Revisas la plantilla que te enseña. Si te parece bien, compila con `platform/3ds/docker-build-test.sh NN`.
3. Haces las pasadas en la consola: un archivo de control por pasada, 60 segundos de espera, foto, y `log.txt` renombrado a `log-A.txt`, `log-B.txt`…
4. Le pasas los logs. Ella ejecuta `analiza-log.py`, compara con la plantilla y actualiza `STATUS.md`.
5. Si en dos pruebas seguidas no se descarta ninguna hipótesis, lleva `STATUS.md` a un modelo grande (Claude) para diseñar la siguiente.

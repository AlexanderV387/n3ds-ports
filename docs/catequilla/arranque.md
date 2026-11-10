# Poner en marcha la nueva Catequilla (una sola vez)

Todo en la **terminal de Ubuntu**, salvo donde dice PowerShell. Ollama tiene que estar abierto en Windows.

## 1. Configuración de OpenCode (hecho el 10 nov. 2026)

- `presence_penalty` en 0 en `~/.config/opencode/opencode.json`.
- `~/.config/opencode/agents/catequilla.md` con `model: ollama/qwen3.6:27b-coding`.
- `/reload` en OpenCode.

## 2. Compilador de 3DS dentro de Ubuntu

```sh
sudo apt update
sudo apt install -y build-essential cmake ninja-build python3 zip git wget libsdl2-dev
wget https://apt.devkitpro.org/install-devkitpro-pacman
chmod +x install-devkitpro-pacman
sudo ./install-devkitpro-pacman
sudo dkp-pacman -S 3ds-dev
source /etc/profile.d/devkit-env.sh
echo $DEVKITPRO        # debe decir /opt/devkitpro
```

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
platform/3ds/build-sdl2-3ds.sh          # unos minutos, una sola vez
```

## 5. Las instrucciones nuevas

```sh
cp ~/catequilla/AGENTS.md ~/catequilla/AGENTS.md.antes-10nov
cp ~/work/3ds-ports/n3ds-ports/docs/catequilla/AGENTS.md ~/catequilla/AGENTS.md
opencode service restart
```

## 6. Primera conversación nueva

Abre una conversación **nueva** (no sigas la de "prueba 8"), con el agente Catequilla, y pégale esto:

> Hola Catequilla. Empezamos con instrucciones y herramientas nuevas. Lee ~/catequilla/AGENTS.md y sigue sus pasos de inicio: lee platform/3ds/STATUS.md en ~/work/3ds-ports/gzdoom-3ds (rama uzdoom-3ds-test25), y hechos-3ds.md y plantilla-prueba.md en ~/work/3ds-ports/n3ds-ports/docs/catequilla/. La prueba 25 ya está escrita y su plan está en STATUS.md. Compílala con `platform/3ds/build-test.sh 25` (nada de MSYS2 ni de copiar a C:). Cuando termine, dame la ruta del .3dsx y la hoja de pasadas A, B, C y D. No cambies código.

## 7. Cada prueba siguiente

1. Conversación nueva con Catequilla: "Lee STATUS.md y prepara la prueba NN según la plantilla".
2. Revisas la plantilla que te enseña. Si te parece bien, compila con `build-test.sh NN`.
3. Haces las pasadas en la consola: un archivo de control por pasada, 60 segundos de espera, foto, y `log.txt` renombrado a `log-A.txt`, `log-B.txt`…
4. Le pasas los logs. Ella ejecuta `analiza-log.py`, compara con la plantilla y actualiza `STATUS.md`.
5. Si en dos pruebas seguidas no se descarta ninguna hipótesis, lleva `STATUS.md` a un modelo grande (Claude) para diseñar la siguiente.

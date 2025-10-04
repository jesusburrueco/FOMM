#!/bin/bash
# Crear carpeta del proyecto
mkdir -p first-order-model
cd first-order-model

# Descargar el repositorio completo de FOMM (demo.py, config, modules)
git clone https://github.com/AliaksandrSiarohin/first-order-model.git .

# Descargar checkpoint vox-cpk.pth
wget -O vox-cpk.pth https://huggingface.co/ruslanmv/avatar-renderer/resolve/main/fomm/vox-cpk.pth

# Crear carpeta sup-mat y descargar driving video
mkdir -p sup-mat
wget -O sup-mat/driving.mp4 http://realitycdc.com/wp-content/uploads/2025/10/56a9d25d-e919-4924-82d0-1aa7ffe08b0b.mp4

cd ..
echo "Setup completado ✅"

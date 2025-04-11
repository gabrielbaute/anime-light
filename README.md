# 🎬 Anime Light

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange?logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/anime-light?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/anime-light/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Conversor optimizado de anime a resoluciones ligeras (360p/480p/720p/1080p) usando FFmpeg.**  

Bueno, esta es una solución para las personas que, como yo, tienen realmente poco espacio de almacenamiento pero, aún así, no quieren deshacerse de todos los archivos que tienen. Lo principal para mi era poder hacer streaming de los anime que descargo para Jellyfin, sobre todo a mi teléfono... razón por la cual, no siempre requiero archivos en 1080p, y 480p-720p suele ser un estpandar de calidad aceptable para mi... pero encontrar archivos en 480 o en 720 ligeros (algo que en el anime, que tiene muchos frames fijos o con pocos cambios) es dificil últimamente, así que quise implementar esta solución y me ha funcionado muy bien. Lo siguiente fue implementarla en forma de CLI!

La librería implementa una cli para convertir archivos de anime (esto es importante, **está optimizado para este estilo**, ya que el anime se caracteriza por tener muchas imágenes estáticas entre frame y frame y manejar una tasa de unos 24 cuadros por segundo). Se puede usar tanto como librería como mediante la CLI. De momento se puede convertir a 360p, 480p, 720p y 1080p (es decir, SD y HD).

Sin más, espero que les parezca útil y, si se les ocurre alguna cosa que agregar, estaré encantado de aceptar colaboraciones y/o sugerencias!


## 🚀 Instalación

### Requisitos previos
- **FFmpeg** instalado y en tu `PATH`.  
  ```bash
  # En Linux/macOS (usando Homebrew):
  brew install ffmpeg

  # En Windows (usando Chocolatey):
  choco install ffmpeg
  ```

### Instalar el paquete
```bash
pip install anime-light
```

## 💻 Uso básico

### Comandos principales
| Comando | Descripción |
|---------|-------------|
| `anime-light "video.mp4"` | Convierte a 480p (calidad predeterminada) |
| `anime-light "video.mkv" --resolution 720p` | Convierte a 720p |
| `anime-light "carpeta/" --crf 25` | Procesa todos los videos en una carpeta |

### Opciones avanzadas
```bash
# Convertir a 720p con máxima compresión (archivos pequeños)
anime-light "episodio.mp4" --resolution 720p --crf 26 --preset veryslow

# Especificar directorio de salida personalizado
anime-light "video.mp4" --output-dir "D:/anime_convertido"

# Audio de baja calidad (para ahorrar espacio)
anime-light "video.mp4" --audio-bitrate 64k
```

## 📊 Tabla de parámetros recomendados

| Resolución | CRF Recomendado | Preset   | Uso típico                     |
|------------|-----------------|----------|--------------------------------|
| 360p       | 26-28           | `fast`   | Móviles o streaming limitado   |
| 480p       | 23-25           | `slow`   | Equilibrio calidad-tamaño      |
| 720p       | 20-22           | `slow`   | HD en pantallas pequeñas       |
| 1080p      | 18-20           | `slower` | Full HD en monitores grandes   |

> ℹ️ **Nota**: Valores CRF más bajos = mejor calidad pero mayor tamaño.

## 🛠️ Ejemplos prácticos

### 1. Convertir un solo archivo
```bash
anime-light "Onepiece_Ep1000.mp4" --resolution 480p --crf 24
```
**Estructura de salida**:  
```
./Onepiece_Ep1000[480p].mp4
```

### 2. Procesar una carpeta completa
```bash
anime-light "~/anime/Shingeki_no_Kyojin/" --resolution 720p --output-dir "~/converted"
```
**Estructura de salida**:  
```
~/converted/
└── 720p/
    ├── Shingeki_no_Kyojin_Ep1[720p].mp4
    ├── Shingeki_no_Kyojin_Ep2[720p].mp4
    └── ...
```

## 📌 Notas importantes
- ✅ **Formatos soportados**: `.mp4`, `.mkv`, `.avi`, `.mov`.
- ⚠️ **Espacios en rutas**: Usa comillas: `"ruta con espacios/video.mp4"`.
- 🔄 **Sobrescritura**: Los archivos existentes se sobrescriben automáticamente en el output, pero no se toca los archivos originales. Se genera un directorio "temp" para evitar posibles conflictos y no contaminar el directorio de salida.

## 🐛 Reportar problemas
¿Encontraste un error? ¡Abre un [issue](https://github.com/gabrielbaute/anime-light/issues) en GitHub!

## 📜 Licencia
MIT © [Gabriel Baute](https://github.com/gabrielbaute)
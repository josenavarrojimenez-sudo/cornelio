# 🎯 Presets de Modelos - Cornelio.app

Colección de configuraciones de modelos optimizadas por caso de uso.

## 📦 Presets Disponibles

| Preset | Uso | Primary | Fallbacks |
|--------|-----|---------|-----------|
| `coding` | Desarrollo, código, debugging | `kimi-k2.5` (OpenRouter) | 3 |
| `frontend` | Diseño web, UI/UX, HTML/CSS | `gemini-3-flash-preview` | 7 |
| `web-search` | Búsqueda web, research | `seed-2.0-lite` | 2 |
| `razonar` | Razonamiento complejo, lógica | `minimax-m2.5:cloud` | 3 |
| `chat` | Conversación natural | `qwen3.5` (Ollama) | 1 |
| `matematicos` | Cálculos, problemas matemáticos | `qwen3.6-plus` | 2 |
| `financieros` | Análisis financiero, economía | `qwen3.6-plus` | 3 |
| `imagenes` | Análisis/generación de imágenes | `gemini-3.1-flash-image` | 2 |
| `videos` | Análisis/generación de video | `veo-3.1` | 4 |
| `principales` | Uso general | `glm-5.1:cloud` | 3 |

## 🚀 Cómo Usar

### Comando Rápido
```bash
# Aplicar preset a un agente
python3 /root/.openclaw/workspace/presets/modelos/apply.py coding cornelio
```

### Desde Cornelio o Magnum
Decí:
- *"Activá el preset de coding"*
- *"Cambiar a preset frontend"*
- *"Usar preset de matemáticos"*

## 📁 Estructura

```
presets/modelos/
├── README.md           - Este archivo
├── apply.py            - Script para aplicar presets
├── coding.json         - Desarrollo
├── frontend.json       - Diseño web/UI-UX
├── web-search.json     - Búsqueda web
├── razonar.json        - Razonamiento
├── chat.json           - Conversación
├── matematicos.json    - Matemáticas
├── financieros.json    - Finanzas
├── imagenes.json       - Imágenes
└── videos.json         - Videos
```

## 📝 Formato JSON

Cada preset sigue esta estructura:

```json
{
  "name": "Nombre del Preset",
  "description": "Descripción del caso de uso",
  "models": {
    "primary": "provider/modelo:tag",
    "fallbacks": [
      "provider/modelo1:tag",
      "provider/modelo2:tag"
    ]
  }
}
```

## 🔧 Proveedores

- `ollama/` - Ollama Cloud (https://ollama.com)
- `openrouter/` - OpenRouter (https://openrouter.ai)

---

**Creado:** 2026-04-15  
**Mantenimiento:** Cornelio + Magnum

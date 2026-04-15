# 🎯 Guía de Presets para Cornelio y Magnum

## 📦 Presets Disponibles

| Comando | Preset | Uso |
|---------|--------|-----|
| `"activá preset coding"` | coding | Desarrollo, código, debugging |
| `"activá preset frontend"` | frontend | Diseño web, UI/UX, HTML/CSS |
| `"activá preset web-search"` | web-search | Búsqueda web, research |
| `"activá preset razonar"` | razonar | Razonamiento complejo, lógica |
| `"activá preset chat"` | chat | Conversación natural |
| `"activá preset matemáticos"` | matematicos | Cálculos, problemas matemáticos |
| `"activá preset financieros"` | financieros | Análisis financiero, economía |
| `"activá preset imágenes"` | imagenes | Análisis/generación de imágenes |
| `"activá preset videos"` | videos | Análisis/generación de video |
| `"activá preset principales"` | principales | Uso general (default) |

## 🚀 Cómo Aplicar un Preset

### Opción 1: Script Directo
```bash
python3 /root/.openclaw/workspace/presets/modelos/apply.py <preset> <agente>
```

Ejemplos:
```bash
# Aplicar preset de coding a Cornelio
python3 /root/.openclaw/workspace/presets/modelos/apply.py coding cornelio

# Aplicar preset de frontend a Cleo
python3 /root/.openclaw/workspace/presets/modelos/apply.py frontend cleo

# Aplicar preset de chat a Magnum
python3 /root/.openclaw/workspace/presets/modelos/apply.py chat magnum
```

### Opción 2: Desde el Chat
Cuando Jose diga:
- *"Quiero los presets de coding"* → Ejecutar script con preset `coding`
- *"Cambiar a preset frontend"* → Ejecutar script con preset `frontend`
- *"Usar preset de matemáticos"* → Ejecutar script con preset `matematicos`

## 📋 Flujo de Trabajo

1. **Jose solicita preset** → Ej: *"Activá preset de coding"*
2. **Cornelio/Magnum ejecuta script** → `apply.py coding cornelio`
3. **Reiniciar gateway** → `openclaw gateway restart`
4. **Confirmar a Jose** → *"Preset de coding aplicado a Cornelio ✅"*

## 🔧 Archivos

- **Presets:** `/root/.openclaw/workspace/presets/modelos/*.json`
- **Script:** `/root/.openclaw/workspace/presets/modelos/apply.py`
- **README:** `/root/.openclaw/workspace/presets/modelos/README.md`

## 📝 Notas

- Los presets modifican `models.json` del agente
- Requiere restart del gateway para aplicar
- Backup automático no incluido → hacer backup manual si es crítico
- Lista de presets: `python3 apply.py --list`

---

**Actualizado:** 2026-04-15  
**Responsable:** Cornelio + Magnum

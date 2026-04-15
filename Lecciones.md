# Lecciones.md - Procesos y Aprendizajes de Cornelio.app

**Creado:** 2026-04-12
**Propósito:** Documentar procesos resueltos, soluciones técnicas, patrones de éxito y errores para referencia futura.

---

## Índice de Lecciones

### 1. Configuración TTS Independiente (2026-04-11)
**Problema:** Gateway TTS usaba una sola voz global para todos los agentes.
**Solución:** Crear scripts TTS independientes por agente con ElevenLabs API directa.
**Archivos:**
- `scripts/audio/cornelio_tts_directo.py` (Voice ID: VAULT:1Password/ElevenLabs/Cornelio-Voice-ID)
- `workspace-magnum/scripts/audio/magnum_tts_directo.py` (Voice ID: aviXFY7Zd7b9DnCUwaCh)
**Lecciones:**
- Gateway TTS `auto: "off"` para evitar conflictos
- FFmpeg boost 1.5x para volumen adecuado
- Formato OGG Opus nativo para Telegram/WhatsApp

---

### 2. Bypass Anti-Bot de Uber Eats (2026-04-12)
**Problema:** Uber Eats bloquea scraping con Cloudflare challenge + bot detection.
**Solución:** Usar Playwright con mobile viewport + deep scroll technique.
**Técnicas:**
- Mobile viewport (412x915) para bypass anti-bot
- Deep scroll con bounce (scroll down + reset + repeat)
- User-agent mobile realista
- Wait times estratégicos para lazy loading
**Skill Creado:** `menu-scraper` (ubicado en `workspace-magnum/skills/`)
**Resultado:** 86 items de menú + 75 imágenes extraídas de Woods Pizza

---

### 3. Comunicación Audio ↔ Texto (2026-04-12)
**Problema:** Confusión sobre cuándo usar audio vs texto.
**Reglas Establecidas:**
- Audio → Audio (vía script TTS directo)
- Texto → Texto (sin audio)
- Modo Trabajo: Siempre texto (activado por Jose)
- Nunca mezclar ambos en misma respuesta

### 3.1 Envío de Audios por API de Telegram (2026-04-12)
**Problema:** Las etiquetas `MEDIA:/ruta/archivo.ogg` en las respuestas de OpenClaw NO se renderizan como notas de voz en Telegram — aparecen como texto plano.
**Solución:** Enviar el audio directamente usando curl con la API de Telegram:
```bash
curl -s -X POST "https://api.telegram.org/bot<BOT_TOKEN>/sendVoice" \
  -F chat_id="<CHAT_ID>" \
  -F voice="@/ruta/al/archivo.ogg"
```
**Implementación:**
1. Generar audio con `scripts/audio/cornelio_tts_directo.py`
2. Enviar por curl directo a Telegram (no usar标签 `MEDIA:`)
3. El audio llega como nota de voz real (duration, mime_type, file_id)
**Lecciones:**
- OpenClaw no procesa automáticamente las etiquetas MEDIA: como archivos de voz
- Siempre usar curl directo para enviar notas de voz en Telegram
- Verificar que el archivo sea .ogg con formato opus_48000_128
**Archivos Involucrados:**
- `scripts/audio/cornelio_tts_directo.py` — generación de audio
- `scripts/audio/generar_respuesta_opus.py` — script auxiliar

---

### 4. Estructura de Skills OpenClaw (2026-04-12)
**Patrón:** Cada skill debe tener:
- `SKILL.md` con YAML frontmatter (name, description)
- Carpeta `scripts/` con herramientas ejecutables
- Carpeta `references/` con documentación técnica
- Package con `skill-creator/scripts/package_skill.py`
**Ejemplo:** `uber-eats-scraper` documenta scraping de cualquier sitio web dinámico

---

## Próximas Lecciones por Documentar

- [ ] Integración de agentes con Mission Control dashboard
- [ ] Flujo de trabajo multi-agente en grupo "Los Menudos"
- [ ] Configuración de workers para tareas asíncronas (Asterix)

---

**Nota:** Actualizar este archivo después de cada tarea significativa resuelta.

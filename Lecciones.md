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

### 2. Voice ID Global Override - Patrón Magnum (2026-04-15)
**Problema:** Per-workspace `openclaw.json` con `auto: "inbound"` y `voiceId` NO funciona. El gateway ignora la Voice ID del workspace y usa la global por defecto.
**Root Cause:** Cuando `auto: "inbound"` está activo, el gateway busca la configuración global de TTS y usa el `voiceId` global (Cornelio: `iwd8AcSi0Je5Quc56ezK`), ignorando por completo el `voiceId` del workspace.
**Solución definitiva (Patrón Magnum):**
1. Global TTS: `auto: "off"` en `/root/.openclaw/openclaw.json`
2. Per-workspace: `auto: "off"` en cada `workspace-{agente}/openclaw.json`
3. Cada agente usa su PROPIO script TTS Python (`{agente}_tts_directo.py`) que llama directamente a ElevenLabs API con su Voice ID única
4. Cada agente tiene un script bash (`{agente}_enviar_audio.sh`) que: genera el audio + lo envía via curl al bot de Telegram del agente
5. El agente responde `NO_REPLY` al sistema para que no envíe texto adicional

**Voice IDs por agente:**
| Agente | Voice ID | Script TTS |
|--------|----------|------------|
| Cornelio | iwd8AcSi0Je5Quc56ezK | cornelio_tts_directo.py |
| Magnum | aviXFY7Zd7b9DnCUwaCh | magnum_tts_directo.py |
| Flavia | a0MaQpDjx7p7bZmqzFp1 | flavia_tts_directo.py |
| Prolix | HJZsH9Tm3FtUeJzIjWVE | prolix_tts_directo.py |
| Ábaco | kulszILr6ees0ArU8miO | abaco_tts_directo.py |
| Cleo | MD6rLAhozcrmkdMZeOBt | cleo_tts_directo.py |

**Lecciones:**
- `auto: "inbound"` en per-workspace NO funciona para voice independence
- El gateway SIEMPRE usa la Voice ID global cuando auto está activo
- La ÚNICA solución es bypass total del gateway: script propio + curl + NO_REPLY
- NO usar `[[tts]]` tags del gateway (está en auto: off)
- Cada agente DEBE usar su propio bot token de Telegram para enviar audio

---

### 1.1 Identidad Vocal Independiente por Agente (2026-04-15)
**Problema:** Cada agente necesita SU PROPIA voz (no compartir la misma).
**Solución:** Crear `openclaw.json` independiente en CADA workspace con config TTS local.
**Patrón Oficial:** https://github.com/josenavarrojimenez-sudo/Magnum/blob/main/docs/TTS_VOICE_CONFIGURATION.md

**Archivos Creados:**
```json
// /root/.openclaw/workspace-magnum/openclaw.json
{
  "messages": {
    "tts": {
      "auto": "inbound",
      "provider": "elevenlabs",
      "providers": {
        "elevenlabs": {
          "apiKey": "aa30f405ec0c1ce39707fbf76436b6c932474c6a5985a5693d363e87c1a899f0",
          "voiceId": "aviXFY7Zd7b9DnCUwaCh",
          "modelId": "eleven_multilingual_v2",
          "languageCode": "es"
        }
      }
    }
  }
}
```

**Agentes Configurados:**
| Agente | Voice ID | Workspace | Estado |
|--------|----------|-----------|--------|
| **Magnum** | `aviXFY7Zd7b9DnCUwaCh` | `/root/.openclaw/workspace-magnum/` | ✅ Activo |
| **Flavia** | `a0MaQpDjx7p7bZmqzFp1` | `/root/.openclaw/workspace-flavia/` | ✅ Activo |
| **Cleo** | `MD6rLAhozcrmkdMZeOBt` | `/root/.openclaw/workspace-cleo/` | ✅ Activo |
| **Prolix** | `HJZsH9Tm3FtUeJzIjWVE` | `/root/.openclaw/workspace-prolix/` | ✅ Activo |
| **Abaco** | `kulszILr6ees0ArU8miO` | `/root/.openclaw/workspace-abaco/` | ✅ Activo |
| **Cornelio** | `iwd8AcSi0Je5Quc56ezK` | `/root/.openclaw/workspace/` | ✅ Activo (`auto: "inbound"`) |

**Lecciones:**
- Cada agente tiene SU PROPIO `openclaw.json` en su workspace
- Config `auto: "inbound"` habilita TTS automático cuando recibe audio
- Voice ID único por agente = identidad vocal independiente
- Gateway global queda en `auto: "off"` (Cornelio ahora tiene su propio openclaw.json con `auto: "inbound"`)
- Script TTS directo como fallback si el gateway no procesa el audio
- **Requiere restart:** `openclaw gateway restart` después de crear configs

**Flujo Operativo (2 caminos):**
```
Camino 1 - Gateway TTS (auto: "inbound"):
1. ✅ Agente recibe audio del usuario
2. ✅ Gateway detecta `auto: "inbound"` en el workspace del agente
3. ✅ Usa el Voice ID específico de ese agente
4. ✅ Genera audio con ElevenLabs automáticamente
5. ✅ Envía audio con la voz propia del agente

Camino 2 - Script TTS directo (fallback/manual):
1. ✅ Recibo audio del usuario
2. ✅ Genero texto de respuesta
3. ✅ Ejecuto script TTS directo (cornelio_tts_directo.py, flavia_tts_directo.py, etc.)
4. ✅ Envío .ogg por curl a Telegram Bot API
5. ✅ Respondo NO_REPLY al sistema
```

**Estructura de Archivos:**
```
/root/.openclaw/
├── openclaw.json                          # GLOBAL: auto: "off" (Cornelio)
├── workspace-magnum/openclaw.json         # auto: "inbound" (Magnum)
├── workspace-flavia/openclaw.json         # auto: "inbound" (Flavia)
├── workspace-cleo/openclaw.json           # auto: "inbound" (Cleo)
├── workspace-prolix/openclaw.json         # auto: "inbound" (Prolix)
├── workspace-abaco/openclaw.json          # auto: "inbound" (Abaco)
└── workspace-*/scripts/audio/
    ├── magnum_tts_directo.py
    ├── flavia_tts_directo.py
    ├── cleo_tts_directo.py
    ├── prolix_tts_directo.py
    └── abaco_tts_directo.py
```

**Comandos de Verificación:**
```bash
# Verificar estado del gateway
openclaw gateway status

# Verificar config global
cat /root/.openclaw/openclaw.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('messages',{}).get('tts',{}))"

# Verificar config de un agente
cat /root/.openclaw/workspace-magnum/openclaw.json | python3 -m json.tool

# Reiniciar gateway para aplicar cambios
openclaw gateway restart
```

**Problema Identificado y Resuelto:**
```
🔧 Problema: TTS global usaba una sola voz para todos los agentes
🔧 Solución 1: Desactivar TTS automático global (auto: "off")
🔧 Solución 2: Crear openclaw.json local en cada workspace
🔧 Solución 3: Configurar auto: "inbound" + Voice ID único por agente
✅ Resultado: CADA AGENTE CON SU VOZ PROPIA
```

**Referencias:**
- https://github.com/josenavarrojimenez-sudo/Magnum/blob/main/docs/TTS_VOICE_CONFIGURATION.md
- https://github.com/josenavarrojimenez-sudo/Magnum/blob/main/docs/MAGNUM_IDENTITY_INTEGRATION.md
- https://github.com/josenavarrojimenez-sudo/Magnum/blob/main/docs/FLUJO_AUDIO_CORNELIO.md

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

- [x] ✅ Corrección de binding faltante para agente Arwen (2026-04-16)
- [ ] Integración de agentes con Mission Control dashboard
- [ ] Flujo de trabajo multi-agente en grupo "Los Menudos"
- [ ] Configuración de workers para tareas asíncronas (Asterix)

## 5. Creación y Configuración de Agente Independiente (Arwen - La Comarca) (2026-04-16)

**Problema:** Se creó el agente Arwen pero los mensajes de Telegram caían en Cornelio en lugar de Arwen.

**Root Cause:** Arwen estaba definido en `openclaw.json` global con `id: "arwen"` y su cuenta de Telegram configurada, pero faltaba el binding que relaciona accountId "arwen" con el agentId "arwen".

**Síntomas:**
- En `sessions_list` aparecían sesiones como `agent:cornelio:telegram:arwen:...` en lugar de `agent:arwen:telegram:...`
- Cuando Jose escribía a @ArwenBot en Telegram, respondía Cornelio en lugar de Arwen.

**Solución:**
1. Agregar binding en `/root/.openclaw/openclaw.json`:
```json
{
  "agentId": "arwen",
  "match": {
    "channel": "telegram",
    "accountId": "arwen"
  }
}
```
2. Reiniciar gateway (con autorización de Jose)
3. Verificar que las nuevas sesiones aparezcan como `agent:arwen:telegram:direct:...`

**Estructura de workspace creada para Arwen:**
- `SOUL.md` – Persona como salonera de La Comarca (tema LOTR)
- `USER.md` – Datos del restaurante (105 productos, 14 categorías temáticas)
- `IDENTITY.md` – Nombre, vibe, emoji
- `AGENTS.md` – Misión y responsabilidades
- `CONFIG.md` – Configuraciones técnicas
- `TOOLS.md` – Herramientas permitidas
- `HEARTBEAT.md` – Tareas periódicas específicas
- `skills.md` + `skills/arwen-restaurant-skill/SKILL.md`
- `scripts/audio/arwen_tts_directo.py` + `arwen_enviar_audio.sh` – TTS independiente (Voice ID: crQgCQuWgUucmYHEPsrB)
- `la-comarca-data/menus/menu_completo.json` – Menú descargado del GitHub repo
- Eliminación de datos de Woods Pizza (copy accidental de Flavia)

**Pendiente (Jose completar):**
- Teléfono, dirección exacta, horarios de las dos sedes
- Instagram oficial de La Comarca ✅ (ya se tiene: @lacomarcarestaurante)
- Configurar pasarela de pago OnVo (o alternativa)
- Configurar Prolix para generar/subir datos de Facebook/Instagram de La Comarca al repo
- Probar flujo completo de Arwen (pedido, pago, audio)

**Lecciones:**
1. Los bindings en `openclaw.json` son CRÍTICOS para enrutar mensajes al agente correcto
2. Sin binding, los mensajes caen en el agente por defecto (Cornelio)
3. Siempre verificar `sessions_list` después de crear un nuevo agente para confirmar enrutamiento correcto
4. Los agentes requieren sus propios scripts de audio independientes (aunque compartan Voice ID)
5. Limpiar datos heredados de otros agentes (workspace isolation)

---

**Nota:** Actualizar este archivo después de cada tarea significativa resuelta.

### 5.2 Actualización Automática de Datos desde GitHub (2026-04-16)

**Patrón:** Replicar el flujo de Flavia, que actualiza datos de Woods Pizza diariamente desde el repo GitHub.

**Cómo funciona Flavia:**
- Script: `/root/.openclaw/workspace-flavia/scripts/update_woods_data.sh`
- Cron: `0 16 * * *` (16:00 UTC = 10:00 AM Costa Rica)
- Hace `git pull` de `https://github.com/josenavarrojimenez-sudo/restaurantes.git`
- Copia `woods-pizza-data/` desde el repo a su workspace local
- Ejecuta cleanup de archivos antiguos
- Flavia lee los datos locales actualizados cada día

**Implementación para Arwen:**
- Script creado: `/root/.openclaw/workspace-arwen/scripts/update_lacomarca_data.sh`
- Cron: `0 16 * * *` (misma hora que Flavia)
- Hace pull del repo GitHub
- Copia:
  - `la-comarca/menus/menu_completo.json` → `la-comarca-data/menus/`
  - `la-comarca/facebook/` → `la-comarca-data/facebook/` (datos scrapeados por Prolix)
  - `la-comarca/imagenes/` → `la-comarca-data/imagenes/`
- Logs: `/root/.openclaw/workspace-arwen/logs/lacomarca_data_update_*.log`
- HEARTBEAT de Arwen actualizado para monitorear esta tarea diaria

**Estado:** ✅ Script funcionando, cron configurado, copia de datos verificada

**Lecciones:**
1. Patrón escalable: cada agente tiene su script de `update_*_data.sh` que actualiza su propio dataset desde el repo central
2. Datos maestros en GitHub → agents los copian localmente → agentes consumen datos locales
3. Agenda de actualización: diaria (16:00 UTC) asegura info fresca sin cargar el repo en cada conversación
4. Separación de responsabilidades: Prolix scrapea y sube al repo (o genera datos), agents consumen via pull
5. Logs separados por agente facilitan debugging

**Próximo paso:**
- Configurar Prolix para que genere los datos de Facebook/Instagram y los suba al repo de GitHub (o los copie localmente)
- Arwen ya está preparado para consumirlos automáticamente

---

**Nota:** Actualizar este archivo después de cada tarea significativa resuelta.

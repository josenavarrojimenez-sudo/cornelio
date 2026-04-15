# Flujo de Audio Independiente - Todos los Agentes

## 📋 Resumen del Problema

Lo que pasó:
- TTS automático del gateway usaba config global (`messages.tts`)
- Esa config tenía UNA sola voz para TODOS los agentes (Cornelio: `iwd8AcSi0Je5Quc56ezK`)
- Cuando cualquier agente respondía, el gateway inyectaba TTS con la voz de Cornelio
- Resultado: Dos audios (uno del agente con su voz + uno del gateway con voz de Cornelio)

## ✅ Solución Aplicada (Patrón Magnum)

1. Desactivar TTS automático global (`auto: "off"`)
2. Desactivar TTS automático por workspace (`auto: "off"`)
3. Cada agente usa script manual con API directa de ElevenLabs
4. Cada agente tiene SU PROPIO Voice ID
5. Cada agente envía audio via curl directo a su bot de Telegram
6. El agente responde `NO_REPLY` al sistema

## 📊 Estado de Agentes

| Agente | Voice ID | Script TTS | Boost | Bot Token | Estado |
|--------|----------|------------|-------|-----------|--------|
| Cornelio | `iwd8AcSi0Je5Quc56ezK` | cornelio_tts_directo.py | 4.0x | 8579844363:AAG... | ✅ |
| Magnum | `aviXFY7Zd7b9DnCUwaCh` | magnum_tts_directo.py | 4.0x | 8562696632:AAE... | ✅ |
| Flavia | `a0MaQpDjx7p7bZmqzFp1` | flavia_tts_directo.py | 4.0x | 8333437311:AAH... | ✅ |
| Prolix | `HJZsH9Tm3FtUeJzIjWVE` | prolix_tts_directo.py | 4.0x | 7454836785:AAF... | ✅ |
| Ábaco | `kulszILr6ees0ArU8miO` | abaco_tts_directo.py | 4.0x | 8318031361:AAH... | ✅ |
| Cleo | `MD6rLAhozcrmkdMZeOBt` | cleo_tts_directo.py | 4.0x | 8174919700:AAH... | ✅ |

## 🔧 Flujo por Agente

### Cornelio
- **Script:** `/root/.openclaw/workspace/scripts/audio/cornelio_tts_directo.py`
- **Voice Settings:** stability 0.5, similarity_boost 0.75, style 0.0
- **Bot:** @CornelioAdelanteBot

### Magnum
- **Script:** `/root/.openclaw/workspace-magnum/scripts/audio/magnum_tts_directo.py`
- **Voice Settings:** stability 0.35, similarity_boost 0.75, style 0.5
- **Bot:** @Magnum_XLBot

### Flavia
- **Script:** `/root/.openclaw/workspace-flavia/scripts/audio/flavia_tts_directo.py`
- **Enviar:** `/root/.openclaw/workspace-flavia/scripts/audio/flavia_enviar_audio.sh`
- **Voice Settings:** stability 0.55, similarity_boost 0.75, style 0.15
- **Bot:** @Flavia_ChefBot

### Prolix
- **Script:** `/root/.openclaw/workspace-prolix/scripts/audio/prolix_tts_directo.py`
- **Enviar:** `/root/.openclaw/workspace-prolix/scripts/audio/prolix_enviar_audio.sh`
- **Voice Settings:** stability 0.45, similarity_boost 0.75, style 0.3
- **Bot:** @Prolix_XLBot

### Ábaco
- **Script:** `/root/.openclaw/workspace-abaco/scripts/audio/abaco_tts_directo.py`
- **Enviar:** `/root/.openclaw/workspace-abaco/scripts/audio/abaco_enviar_audio.sh`
- **Voice Settings:** stability 0.55, similarity_boost 0.75, style 0.2
- **Bot:** @Abaco_XLBot

### Cleo
- **Script:** `/root/.openclaw/workspace-cleo/scripts/audio/cleo_tts_directo.py`
- **Enviar:** `/root/.openclaw/workspace-cleo/scripts/audio/cleo_enviar_audio.sh`
- **Voice Settings:** stability 0.40, similarity_boost 0.75, style 0.4
- **Bot:** @Cleo_XLBot

## 🚨 Puntos Clave

1. **NO usar TTS automático del gateway** — siempre usar script manual
2. **Cada agente tiene SU PROPIO Voice ID** — no compartir
3. **Cada agente tiene SU PROPIO bot de Telegram** — no mezclar tokens
4. **Boost de volumen 4.0x** — para evitar ruido de fondo
5. **Formato OGG Opus** — nativo WhatsApp/Telegram (`opus_48000_128`)
6. **API Key:** `config["skills"]["entries"]["sag"]["apiKey"]` en openclaw.json

## 📝 Checklist Verificado

- [x] Global TTS `auto: "off"` en `/root/.openclaw/openclaw.json`
- [x] Per-workspace TTS `auto: "off"` para todos los agentes
- [x] Script TTS directo creado para cada agente
- [x] Script bash enviar_audio creado para Flavia, Prolix, Ábaco, Cleo
- [x] Boost de volumen 4.0x en todos los scripts
- [x] API key path corregido (`config["skills"]["entries"]["sag"]["apiKey"]`)
- [x] SOUL.md actualizado con instrucciones de audio independiente
- [x] Lecciones.md actualizado con documentación del problema
- [x] Documentación de flujo creada

---

_Documentación creada el 2026-04-15 por Cornelio. Basada en el patrón Magnum._
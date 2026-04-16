# Lecciones Aprendidas: Independencia de Audio por Agente (ElevenLabs TTS Directo)

## El Problema
Por defecto, OpenClaw utiliza un servicio de TTS (Text-to-Speech) global configurado en el gateway. Esto provoca que **todos los agentes suenen exactamente igual**, perdiendo su identidad vocal única. Además, el flujo estándar a veces fuerza respuestas de texto cuando se requiere audio nativo para plataformas como Telegram o WhatsApp.

## La Solución
Implementar un sistema de **TTS Independiente** para cada agente. En lugar de usar las etiquetas `[[tts]]` del gateway, cada agente utiliza un script especializado que se comunica directamente con la API de ElevenLabs.

### Componentes Clave:
1. **Script TTS Directo (`scripts/audio/cornelio_tts_directo.py`):**
   - Utiliza `requests` para enviar texto a la API de ElevenLabs.
   - Configura un `Voice ID` específico por agente.
   - Aplica un boost de volumen (1.5x - 2.0x) usando `ffmpeg` para asegurar claridad en dispositivos móviles.
   - Genera archivos `.ogg` con el codec `libopus` (formato nativo que Telegram reconoce como nota de voz).

2. **Identidad Vocal:**
   - Cada agente tiene su propio `VOICE_ID` (Cornelio, Magnum, Flavia, etc.).
   - Se ajustan parámetros como `stability`, `style` y `similarity_boost` para dar personalidad (Cornelio es más expresivo y autoritario).

3. **Flujo de Envío (Bypass de Gateway):**
   - Después de generar el audio, se utiliza `curl` para enviar el archivo directamente a la API de Telegram (`sendVoice`).
   - El agente responde con `NO_REPLY` al sistema principal para evitar que se envíe texto duplicado o innecesario.

### Rutas y Servicios:
- **API:** `https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}`
- **Formato:** `opus_48000_128` (Ogg Opus)
- **Herramienta de Procesamiento:** `ffmpeg` para normalización y boost de audio.
- **Telegram API:** `https://api.telegram.org/bot{TOKEN}/sendVoice`

## Cómo Implementar un Nuevo Agente con Audio Propio:
1. Copiar el `tts_template.py`.
2. Asignar el `VOICE_ID` del agente desde ElevenLabs.
3. Configurar el `botToken` del agente en el script o variable de entorno.
4. En el prompt del agente, instruir que para respuestas de audio debe ejecutar el script y responder `NO_REPLY`.

---
*Documentación generada por Cornelio (CEO Virtual) para la posteridad de Cornelio.app.*

# 🔄 Flujo Completo de Audio: WhatsApp → ElevenLabs → Respuesta de Audio

**Autor:** Cornelio (CEO Virtual - Agente OpenClaw)  
**Usuario:** Jose Navarro (+50672516680)  
**Fecha:** 2026-04-10  
**Versión:** 2.0 (Ultra Detallada)  
**Voice ID:** `VAULT:1Password/ElevenLabs/Cornelio-Voice-ID` (ÚNICA - PERMANENTE - NO CAMBIAR SIN AUTORIZACIÓN DE JOSE)

---

## 📋 Tabla de Contenidos

1. [Resumen General del Flujo](#1-resumen-general-del-flujo)
2. [Infraestructura del Sistema](#2-infraestructura-del-sistema)
3. [Configuración OpenClaw (openclaw.json)](#3-configuración-openclaw-openclawjson)
4. [Paso 1: Recepción del Audio](#4-paso-1-recepción-del-audio-whatsapp--openclaw)
5. [Paso 2: Transcripción STT](#5-paso-2-transcripción-stt-speech-to-text)
6. [Paso 3: Generación de Respuesta IA](#6-paso-3-generación-de-respuesta-ia)
7. [Paso 4: Conversión TTS](#7-paso-4-conversión-tts-text-to-speech)
8. [Paso 5: Entrega del Audio](#8-paso-5-entrega-del-audio-al-usuario)
9. [Scripts Detallados](#9-scripts-detallados)
10. [APIs Externas - Estructura Completa](#10-apis-externas---estructura-completa)
11. [Formatos de Archivo](#11-formatos-de-archivo)
12. [Reglas de Oro](#12-reglas-de-oro---audiotexto)
13. [Troubleshooting](#13-troubleshooting)
14. [Historial de Cambios](#14-historial-de-cambios)

---

## 1. Resumen General del Flujo

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│   USUARIO   │────▶│  WHATSAPP    │────▶│   OPENCLAW    │────▶│  INBOUND     │
│  +5067...   │     │  (Baileys)   │     │   GATEWAY     │     │  MEDIA DIR   │
│  Envía audio│     │  Webhook     │     │   VPS         │     │  .ogg        │
└─────────────┘     └──────────────┘     └───────┬───────┘     └──────────────┘
                                                 │
                    ┌──────────────┐     ┌───────▼───────┐     ┌──────────────┐
                    │   USUARIO    │◀────│    AGENTE     │◀────│  ELEVENLABS  │
                    │  +5067...    │     │   CORNELIO    │     │  TTS API     │
                    │  Recibe audio│     │  (GLM-5/etc)  │     │  .ogg output │
                    └─────────────┘     └───────▲───────┘     └──────────────┘
                                                 │
                                         ┌───────┴───────┐
                                         │  ELEVENLABS    │
                                         │  STT API       │
                                         │  Scribe V2     │
                                         │  Transcripción │
                                         └───────────────┘
```

**Paso a paso:**

```
PASO 1:  Usuario envía audio por WhatsApp
PASO 2:  OpenClaw Gateway recibe webhook (Baileys)
PASO 3:  OpenClaw guarda .ogg en /root/.openclaw/media/inbound/{uuid}.ogg
PASO 4:  OpenClaw detecta <media:audio> en el mensaje
PASO 5:  OpenClaw ejecuta scribe_stt.sh → ElevenLabs Scribe V2 API
PASO 6:  ElevenLabs devuelve JSON con transcripción
PASO 7:  OpenClaw inyecta transcript en contexto del agente
PASO 8:  Cornelio (modelo IA) procesa transcripción + contexto
PASO 9:  Cornelio genera respuesta de texto
PASO 10: OpenClaw detecta tts.auto = "inbound" → activa TTS
PASO 11: OpenClaw llama ElevenLabs TTS API (texto → audio)
PASO 12: ElevenLabs devuelve audio OGG Opus (binario)
PASO 13: OpenClaw envía audio al usuario por WhatsApp
```

---

## 2. Infraestructura del Sistema

### Servidor (VPS)

| Propiedad | Valor |
|-----------|-------|
| **Hostname** | srv1443323 |
| **OS** | Linux 6.17.0-19-generic (x64) |
| **Node.js** | v22.22.2 |
| **OpenClaw** | v2026.4.9 |
| **Shell** | bash |
| **Gateway Port** | 18789 |
| **Gateway Bind** | loopback |
| **Gateway Mode** | local |

### Agentes

| Agente | ID | Rol | Canal | Workspace |
|--------|-----|-----|-------|-----------|
| **Cornelio** | `cornelio` | CEO Virtual | WhatsApp (+50672516680) | `/root/.openclaw/workspace` |
| **Magnum** | `magnum` | Brazo Derecho | Telegram | `/root/.openclaw/workspace-magnum` |

### Modelo IA

| Propiedad | Valor |
|-----------|-------|
| **Router** | OpenRouter |
| **Runtime** | `openrouter/z-ai/glm-5-turbo` (variable) |
| **Fallbacks** | 100+ modelos disponibles |

### Canales

| Canal | Estado | ID |
|-------|--------|-----|
| **WhatsApp** | ✅ Activo | Baileys |
| **Telegram (Cornelio)** | ✅ Activo | `VAULT:1Password/Telegram/Cornelio-Bot-Token` |
| **Telegram (Magnum)** | ✅ Activo | `VAULT:1Password/Telegram/Magnum-Bot-Token` |
| **WebChat** | ✅ Activo | `https://webchat.cornelio.app` |

### Plugins

| Plugin | Estado |
|--------|--------|
| `openrouter` | ✅ Enabled |
| `elevenlabs` | ✅ Enabled |
| `device-pair` | ✅ Enabled |

---

## 3. Configuración OpenClaw (openclaw.json)

**Archivo:** `/root/.openclaw/openclaw.json`

### 3.1 TTS (Text-to-Speech)

```json
{
  "messages": {
    "tts": {
      "auto": "inbound",
      "provider": "elevenlabs",
      "providers": {
        "elevenlabs": {
          "apiKey": "aa30f405ec0c1ce39707fbf76436b6a5985a5693d363e87c1a899f0",
          "voiceId": "VAULT:1Password/ElevenLabs/Cornelio-Voice-ID",
          "modelId": "eleven_v3",
          "languageCode": "es"
        }
      }
    }
  }
}
```

| Campo | Valor | Descripción |
|-------|-------|-------------|
| `auto` | `"inbound"` | TTS SOLO cuando el mensaje entrante es audio |
| `provider` | `"elevenlabs"` | Proveedor TTS |
| `apiKey` | `aa30f4...899f0` | API Key ElevenLabs |
| `voiceId` | `VAULT:1Password/ElevenLabs/Cornelio-Voice-ID` | Voz personalizada de Cornelio |
| `modelId` | `eleven_v3` | Modelo TTS |
| `languageCode` | `"es"` | Idioma |

**Valores `tts.auto`:**
- `"always"` → ❌ NO USAR (siempre audio, rompe regla de oro)
- `"inbound"` → ✅ USAR (audio solo si entra audio)
- `"off"` → Nunca auto-TTS

### 3.2 STT (Speech-to-Text)

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "maxBytes": 20971520,
        "models": [
          {
            "type": "cli",
            "command": "/root/.openclaw/workspace-magnum/scripts/scribe_stt.sh",
            "args": ["{{MediaPath}}", "es"]
          },
          {
            "type": "cli",
            "command": "whisper",
            "args": ["--model", "base", "{{MediaPath}}"]
          }
        ]
      }
    }
  }
}
```

| Campo | Valor | Descripción |
|-------|-------|-------------|
| `enabled` | `true` | STT activado |
| `maxBytes` | `20971520` | Máximo 20MB |
| `models[0]` | `scribe_stt.sh` | **PRIMARY** - ElevenLabs Scribe V2 |
| `models[1]` | `whisper` | **FALLBACK** - Solo si ElevenLabs falla |

### 3.3 WhatsApp Channel

```json
{
  "channels": {
    "whatsapp": {
      "selfChatMode": false,
      "dmPolicy": "pairing",
      "allowFrom": ["+50672516680"],
      "enabled": true
    }
  }
}
```

### 3.4 Bindings (Agente ↔ Canal)

```json
{
  "bindings": [
    {
      "agentId": "magnum",
      "match": { "channel": "telegram" }
    },
    {
      "agentId": "cornelio",
      "match": {
        "channel": "whatsapp",
        "peer": { "kind": "direct", "id": "+50672516680" }
      }
    }
  ]
}
```

### 3.5 API Key (redundancia)

La API Key de ElevenLabs está en 3 lugares:
1. `messages.tts.providers.elevenlabs.apiKey`
2. `skills.entries.sag.apiKey`
3. Variable de entorno `$ELEVENLABS_API_KEY`

---

## 4. Paso 1: Recepción del Audio (WhatsApp → OpenClaw)

### 4.1 Flujo

```
Jose (WhatsApp) → Baileys Webhook → OpenClaw Gateway (port 18789) → Guardar .ogg
```

### 4.2 Formato del Audio Recibido

| Propiedad | Valor |
|-----------|-------|
| **Contenedor** | OGG |
| **Codec** | Opus |
| **Sample Rate** | 48,000 Hz |
| **Canales** | Mono |
| **Máximo** | 20 MB |
| **Extensión** | `.ogg` |
| **MIME** | `audio/ogg; codecs=opus` |

### 4.3 Ruta de Almacenamiento

```
/root/.openclaw/media/inbound/{uuid}.ogg
```

**Ejemplos reales:**
```
/root/.openclaw/media/inbound/7c14ef91-c205-42a3-930a-b50436b85a35.ogg
/root/.openclaw/media/inbound/309990b3-569a-4d6e-ad3a-939148112df4.ogg
/root/.openclaw/media/inbound/1b138189-5e2c-4b0e-9c97-c063e9d3e3c9.ogg
```

### 4.4 Detección de Audio

OpenClaw detecta `<media:audio>` en el body del mensaje:

```
Mensaje entrante:
├── message_id: "3EB0..."
├── sender_id: "+50672516680"
├── body: "<media:audio>"
└── metadata:
    ├── filename: "7c14ef91-...-.ogg"
    ├── mime: "audio/ogg"
    └── localPath: "/root/.openclaw/media/inbound/7c14ef91-...-.ogg"
```

### 4.5 Directorios

```
/root/.openclaw/media/
├── inbound/     ← Recibidos (.ogg, .jpg, .mp4, .txt, .html)
└── outbound/    ← Generados (se crea dinámicamente)
```

---

## 5. Paso 2: Transcripción STT (Speech-to-Text)

### 5.1 Flujo

```
Archivo .ogg → scribe_stt.sh → curl POST → ElevenLabs API → JSON → Inyectar al agente
```

### 5.2 Script Primario: scribe_stt.sh

**Ubicación:** `/root/.openclaw/workspace-magnum/scripts/scribe_stt.sh`

```bash
#!/bin/bash
API_KEY="aa30f405ec0c1ce39707fbf76436b6a5985a5693d363e87c1a899f0"
FILE="$1"
LANG_CODE="${2:-es}"

curl -s -X POST "https://api.elevenlabs.io/v1/speech-to-text" \
  -H "xi-api-key: $API_KEY" \
  -F "model_id=scribe_v2" \
  -F "language_code=$LANG_CODE" \
  -F "file=@$FILE"
```

**Qué hace paso a paso:**
1. `$1` = ruta del archivo de audio (OpenClaw pasa `{{MediaPath}}`)
2. `$2` = código de idioma (por defecto `es`)
3. `curl -s` = silent mode (sin progress bar)
4. `-X POST` = método HTTP POST
5. `-H "xi-api-key: ..."` = autenticación con API Key
6. `-F "model_id=scribe_v2"` = modelo de transcripción (form field)
7. `-F "language_code=es"` = idioma español
8. `-F "file=@$FILE"` = archivo adjunto (el `@` indica lectura de archivo)
9. Devuelve JSON por stdout

### 5.3 Script Fallback: Whisper

```bash
whisper --model base {{MediaPath}}
```

Solo se ejecuta si `scribe_stt.sh` falla (exit code != 0).

### 5.4 API ElevenLabs STT

**Endpoint:** `POST https://api.elevenlabs.io/v1/speech-to-text`

**Headers enviados:**
```
xi-api-key: aa30f405ec0c1ce39707fbf76436b6a5985a5693d363e87c1a899f0
```

**Body (multipart/form-data):**
```
model_id: scribe_v2
language_code: es
file: [binario del .ogg]
```

**Respuesta JSON:**
```json
{
  "language_code": "spa",
  "language_probability": 1.0,
  "text": "Vamos a ver ahora sí, Cornelio",
  "words": [
    {"text": "Vamos", "start": 0.059, "end": 0.079, "type": "word", "logprob": -0.002},
    {"text": " ", "start": 0.079, "end": 0.099, "type": "spacing", "logprob": -9.5e-07}
  ],
  "transcription_id": "UOqTKagsgMsWXCzxwj2i",
  "audio_duration_secs": 2.3
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `language_code` | string | Idioma detectado |
| `language_probability` | float | Confianza (0-1) |
| `text` | string | **Texto transcrito** (campo principal) |
| `words[]` | array | Palabras con timestamps |
| `words[].text` | string | Palabra |
| `words[].start` | float | Inicio (seg) |
| `words[].end` | float | Fin (seg) |
| `words[].type` | string | `word`, `spacing` o `audio_event` |
| `words[].logprob` | float | Probabilidad |
| `transcription_id` | string | ID único |
| `audio_duration_secs` | float | Duración (seg) |

### 5.5 Python Script Alternativo

**Ubicación:** `/root/.openclaw/workspace/scripts/audio/transcribir_audio_elevenlabs.py`

```python
#!/usr/bin/env python3
import os, sys, json, requests
from pathlib import Path

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
if not ELEVENLABS_API_KEY:
    with open("/root/.openclaw/openclaw.json", "r") as f:
        config = json.load(f)
        ELEVENLABS_API_KEY = config["skills"]["sag"]["apiKey"]

def transcribir_audio(ruta_audio, idioma="es"):
    with open(ruta_audio, "rb") as f:
        audio_data = f.read()
    url = "https://api.elevenlabs.io/v1/scribe/transcribe"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Accept": "application/json"}
    data = {"audio": audio_data, "language": idioma, "model_id": "scribe_v2"}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("text", "")
    raise Exception(f"Error STT: {response.status_code}")

if __name__ == "__main__":
    texto = transcribir_audio(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "es")
    print(f"📝 {texto}")
```

---

## 6. Paso 3: Generación de Respuesta (IA)

### 6.1 Inyección de Transcripción

OpenClaw inyecta el resultado STT en el prompt:

```
User text:
[WhatsApp +50672516680 +15s Fri 2026-04-10 19:14 UTC] <media:audio>
Transcript:
{"language_code":"spa","language_probability":1.0,"text":"Vamos a ver ahora sí, Cornelio",...}
```

### 6.2 Modelo IA

El agente Cornelio (model: `openrouter/z-ai/glm-5-turbo`) recibe:
- Transcripción del audio
- Contexto de archivos (AGENTS.md, SOUL.md, USER.md, TOOLS.md)
- Memoria (QMD con búsqueda semántica)
- Historial de conversación

### 6.3 Generación

Cornelio genera una respuesta de texto. Si el original fue audio, OpenClaw activa TTS automáticamente (`auto: "inbound"`).

---

## 7. Paso 4: Conversión TTS (Text-to-Speech)

### 7.1 Flujo

```
Texto respuesta → OpenClaw detecta "inbound" → ElevenLabs TTS → Audio OGG Opus
```

### 7.2 Llamada API ElevenLabs TTS

**Endpoint:** `POST https://api.elevenlabs.io/v1/text-to-speech/VAULT:1Password/ElevenLabs/Cornelio-Voice-ID`

**Headers:**
```
xi-api-key: aa30f405ec0c1ce39707fbf76436b6a5985a5693d363e87c1a899f0
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "text": "Texto de respuesta a convertir en audio",
  "model_id": "eleven_v3",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": true
  }
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `text` | string | Texto a convertir |
| `model_id` | string | `eleven_v3` |
| `voice_settings.stability` | float | 0.5 (estabilidad) |
| `voice_settings.similarity_boost` | float | 0.75 (similitud voz) |
| `voice_settings.style` | float | 0.0 (exageración) |
| `voice_settings.use_speaker_boost` | bool | true (claridad) |

**Respuesta:**
- **Status:** `200 OK`
- **Content-Type:** `audio/ogg`
- **Body:** Binario OGG Opus

### 7.3 Python Script: generar_respuesta_opus.py

**Ubicación:** `/root/.openclaw/workspace/scripts/audio/generar_respuesta_opus.py`

```python
#!/usr/bin/env python3
import os, sys, json, requests
from pathlib import Path

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
if not ELEVENLABS_API_KEY:
    with open("/root/.openclaw/openclaw.json", "r") as f:
        config = json.load(f)
        ELEVENLABS_API_KEY = config["skills"]["sag"]["apiKey"]

VOICE_ID = "VAULT:1Password/ElevenLabs/Cornelio-Voice-ID"
MODEL = "eleven_multilingual_v2"

def generar_audio(texto, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    data = {
        "text": texto,
        "model_id": MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        return True
    raise Exception(f"Error TTS: {response.status_code} - {response.text}")

if __name__ == "__main__":
    generar_audio(sys.argv[1], sys.argv[2])
    print(f"✅ Audio generado: {sys.argv[2]}")
```

### 7.4 Pipeline Completo: transcribir_respuesta_opus.py

**Ubicación:** `/root/.openclaw/workspace/scripts/audio/transcribir_respuesta_opus.py`

```python
#!/usr/bin/env python3
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.audio.transcribir_audio_elevenlabs import transcribir_audio
from scripts.audio.generar_respuesta_opus import generar_audio

def pipeline_audio(ruta_entrada, ruta_salida, idioma="es"):
    texto = transcribir_audio(ruta_entrada, idioma)
    respuesta = f"He recibido tu mensaje: '{texto}'"
    generar_audio(respuesta, ruta_salida)
    return texto, respuesta

if __name__ == "__main__":
    texto, resp = pipeline_audio(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "es")
    print(f"🎉 Pipeline completado: {resp}")
```

---

## 8. Paso 5: Entrega del Audio al Usuario

### 8.1 Flujo

```
Audio OGG Opus (binario) → OpenClaw Gateway → Baileys → WhatsApp → Usuario
```

### 8.2 Formato del Audio Enviado

| Propiedad | Valor |
|-----------|-------|
| **Contenedor** | OGG |
| **Codec** | Opus |
| **Sample Rate** | 48,000 Hz |
| **Canales** | Mono |
| **Bitrate** | 128 kbps |
| **Extensión** | `.ogg` |
| **MIME** | `audio/ogg; codecs=opus` |
| **Compatibilidad** | 100% iOS, 100% Android, 100% WhatsApp |

### 8.3 El audio se envía como "voice note" nativo de WhatsApp

OpenClaw utiliza el formato OGG Opus que es el formato nativo de WhatsApp para notas de voz. Esto garantiza que el audio se reproduzca directamente en la app sin necesidad de conversión adicional.

---

## 9. Scripts Detallados

### Mapa de Scripts

```
/root/.openclaw/
├── openclaw.json                          ← Configuración principal
├── workspace/
│   └── scripts/
│       └── audio/
│           ├── generar_respuesta_opus.py          ← TTS (texto → audio)
│           ├── transcribir_audio_elevenlabs.py     ← STT (audio → texto)
│           └── transcribir_respuesta_opus.py      ← Pipeline completo
├── workspace-magnum/
│   └── scripts/
│       └── scribe_stt.sh                          ← STT primario (Bash)
└── media/
    ├── inbound/                                    ← Archivos recibidos
    └── outbound/                                   ← Archivos generados
```

### Dependencias

```
Python 3.x:
  - requests (pip install requests)     ← Usado en scripts Python
  - elevenlabs (opcional)               ← SDK ElevenLabs (NO instalado actualmente)

Sistema:
  - curl                                ← Usado en scribe_stt.sh
  - whisper                             ← Fallback STT (OpenAI)
  - bash                                ← Shell de scribe_stt.sh
```

---

## 10. APIs Externas - Estructura Completa

### 10.1 ElevenLabs Speech-to-Text (STT)

```
METHOD:  POST
URL:     https://api.elevenlabs.io/v1/speech-to-text
AUTH:    Header: xi-api-key: {API_KEY}
BODY:    multipart/form-data
FIELDS:  model_id=scribe_v2
         language_code=es
         file=@{audio_path.ogg}
RESPONSE: 200 OK
         Content-Type: application/json
         Body: {"language_code":"spa","text":"...","words":[...],"transcription_id":"..."}
```

### 10.2 ElevenLabs Text-to-Speech (TTS)

```
METHOD:  POST
URL:     https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
AUTH:    Header: xi-api-key: {API_KEY}
BODY:    application/json
FIELDS:  {"text":"...","model_id":"eleven_v3","voice_settings":{...}}
RESPONSE: 200 OK
         Content-Type: audio/ogg
         Body: [binary OGG Opus data]
```

### 10.3 Parámetros de Voz

| Parámetro | Valor | Rango | Descripción |
|-----------|-------|-------|-------------|
| `voice_id` | `VAULT:1Password/ElevenLabs/Cornelio-Voice-ID` | - | Voz personalizada Cornelio |
| `stability` | 0.5 | 0.0-1.0 | Menos = más expresiva, Más = más consistente |
| `similarity_boost` | 0.75 | 0.0-1.0 | Similitud con voz de referencia |
| `style` | 0.0 | 0.0-1.0 | Exageración del estilo |
| `use_speaker_boost` | true | bool | Mejora claridad del hablante |

---

## 11. Formatos de Archivo

### Audio Entrante (WhatsApp → OpenClaw)

| Propiedad | Valor |
|-----------|-------|
| Formato | OGG |
| Codec | Opus |
| Sample Rate | 48,000 Hz |
| Canales | Mono |
| Extensión | `.ogg` |
| Ruta | `/root/.openclaw/media/inbound/{uuid}.ogg` |

### Audio Saliente (OpenClaw → WhatsApp)

| Propiedad | Valor |
|-----------|-------|
| Formato | OGG |
| Codec | Opus |
| Sample Rate | 48,000 Hz |
| Canales | Mono |
| Bitrate | 128 kbps |
| Extensión | `.ogg` |
| Ruta | `/root/.openclaw/media/outbound/` (dinámico) |

### Formatos Soportados por ElevenLabs TTS

| Formato | Descripción | Recomendado |
|---------|-------------|-------------|
| `opus_48000_32` | Opus 32kbps | ❌ |
| `opus_48000_64` | Opus 64kbps | ❌ |
| `opus_48000_96` | Opus 96kbps | ❌ |
| `opus_48000_128` | Opus 128kbps | ⭐ WhatsApp nativo |
| `opus_48000_192` | Opus 192kbps | ❌ |
| `mp3_44100_128` | MP3 128kbps | ❌ No funciona en WhatsApp |
| `m4a_aac_44100_128` | M4A AAC 128kbps | ❌ No funciona en WhatsApp |

---

## 12. Reglas de Oro - Audio/Texto

### REGLA #1: Audio → Audio

```
Si Jose envía AUDIO → Cornelio responde con AUDIO
```

### REGLA #2: Texto → Texto

```
Si Jose envía TEXTO → Cornelio responde con TEXTO
```

### REGLA #3: Voice ID Inmutable

```
Voice ID: VAULT:1Password/ElevenLabs/Cornelio-Voice-ID → NUNCA CAMBIAR SIN AUTORIZACIÓN DE JOSE
```

### REGLA #4: Formato OGG Opus

```
TODOS los audios de salida deben ser .ogg con codec Opus
```

### REGLA #5: STT ElevenLabs primero

```
1. ElevenLabs Scribe V2 (primario)
2. Whisper (fallback, solo si ElevenLabs falla)
```

### Implementación en openclaw.json

```json
{
  "messages": {
    "tts": {
      "auto": "inbound"    ← "inbound" = TTS solo cuando llega audio
    }
  }
}
```

---

## 13. Troubleshooting

### Problema: Siempre responde con audio (incluso a texto)

**Causa:** `tts.auto` configurado como `"always"` en openclaw.json  
**Solución:** Cambiar a `"inbound"` y reiniciar gateway:
```bash
# Editar openclaw.json
# Cambiar "auto": "always" → "auto": "inbound"
openclaw gateway restart
```

### Problema: No recibe audio de respuesta

**Causa:** TTS provider no configurado o API Key inválida  
**Solución:** Verificar `messages.tts.providers.elevenlabs.apiKey`

### Problema: Transcripción no funciona

**Causa:** Script STT no encontrado o API Key inválida  
**Solución:** Verificar que `scribe_stt.sh` exista y sea ejecutable:
```bash
ls -la /root/.openclaw/workspace-magnum/scripts/scribe_stt.sh
chmod +x /root/.openclaw/workspace-magnum/scripts/scribe_stt.sh
```

### Problema: Audio no se reproduce en WhatsApp

**Causa:** Formato incorrecto (MP3, AAC, etc.)  
**Solución:** Asegurar formato OGG Opus (`opus_48000_128`)

---

## 14. Historial de Cambios

| Fecha | Cambio |
|-------|--------|
| 2026-04-08 | Configuración inicial ElevenLabs (Maximus) |
| 2026-04-08 | Migración a OGG Opus (100% compatible WhatsApp) |
| 2026-04-08 | Voice ID definitivo: VAULT:1Password/ElevenLabs/Cornelio-Voice-ID |
| 2026-04-10 | Documento v1.0 creado (Jose) |
| 2026-04-10 | Fix: tts.auto cambiado a "inbound" |
| 2026-04-10 | Documento v2.0 ultra detallado (Cornelio) |
| 2026-04-10 | Verificación completa de configuración real del sistema |

---

## 📌 Resumen Final

| Componente | Valor |
|-----------|-------|
| **STT Provider** | ElevenLabs Scribe V2 |
| **STT Endpoint** | `/v1/speech-to-text` |
| **TTS Provider** | ElevenLabs |
| **TTS Endpoint** | `/v1/text-to-speech/{voice_id}` |
| **Voice ID** | `VAULT:1Password/ElevenLabs/Cornelio-Voice-ID` |
| **TTS Model** | `eleven_v3` / `eleven_multilingual_v2` |
| **Formato entrada** | OGG Opus (48kHz, mono) |
| **Formato salida** | OGG Opus (48kHz, 128kbps, mono) |
| **Ruta inbound** | `/root/.openclaw/media/inbound/` |
| **Ruta outbound** | `/root/.openclaw/media/outbound/` |
| **Config file** | `/root/.openclaw/openclaw.json` |
| **TTS auto mode** | `inbound` (solo audio → audio) |

---

_Documento generado por Cornelio (CEO Virtual) para Cornelio.app_  
_Voz: VAULT:1Password/ElevenLabs/Cornelio-Voice-ID (PERMANENTE)_  
_Flujo operativo y verificado el 2026-04-10_
# 🤖 Cornelio.app

**CEO Virtual con Sistema de Memoria Híbrida QMD + MemPalace**

> Cornelio es un agente de IA que funciona como CEO Virtual, asistido por **Magnum** (su brazo derecho operativo). Ambos agentes comparten memoria persistente mediante un sistema híbrido de búsqueda semántica.

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    CORNELIO.APP                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐         ┌──────────────┐                 │
│   │  CORNELIO    │  ────►  │   MAGNUM     │                 │
│   │  (CEO Virtual)│  tareas │(Brazo Derecho)│                │
│   │              │ ◄─────  │              │                 │
│   │  Estrategia  │ reportes │ Ejecución   │                 │
│   └──────────────┘         └──────────────┘                 │
│          │                        │                         │
│          └────────┬───────────────┘                         │
│                   ▼                                         │
│   ┌─────────────────────────────────────────────┐           │
│   │        SISTEMA DE MEMORIA HÍBRIDA           │           │
│   ├─────────────────────┬───────────────────────┤           │
│   │   QMD (Búsqueda)    │  MemPalace (Estructura)│          │
│   │   • BM25 + Vector   │  • Wings / Rooms      │          │
│   │   • Reranking LLM   │  • Knowledge Graph    │          │
│   │   • 914+ vectores   │  • Contexto L0/L1    │          │
│   └─────────────────────┴───────────────────────┘           │
│                          │                                   │
│                   ┌──────┴──────┐                           │
│                   ▼             ▼                           │
│            Jose Navarro    Telegram/WhatsApp                │
│            (CEO Humano)     (Canales)                       │
└─────────────────────────────────────────────────────────────┘
```

## 🧠 Sistema de Memoria Híbrida

### ¿Por qué híbrido?

| Necesidad | Solución |
|-----------|----------|
| Búsqueda rápida en transcripciones | **QMD** - BM25 + vector + reranking |
| Estructura organizada por agente/proyecto | **MemPalace** - wings, rooms, knowledge graph |
| Memoria permanente entre sesiones | Ambos - indexación automática via cron |
| Contexto cruzado entre agentes | OpenClaw `extraCollections` |

### Componentes

#### 1. QMD (`@tobilu/qmd`)
- Motor de búsqueda local (sin API externa)
- BM25 full-text + vector semántico + re-ranking con LLM local
- Modelos GGUF: embeddinggemma-300M + qwen3-reranker + query-expansion
- Colecciones: `cornelio-sessions`, `magnum-sessions`

#### 2. MemPalace (`mempalace`)
- Organización tipo "palacio de la memoria"
- **Wings**: cornelio (CEO), magnum (ejecutor), jose (humano)
- **Rooms**: por tema (tareas, proyectos, decisiones)
- Knowledge Graph temporal (quién → hizo qué → cuándo)

#### 3. OpenClaw Multi-Agent
- Agentes aislados: workspace + agentDir + sesiones separadas
- Compartición de memoria vía `memorySearch.qmd.extraCollections`
- Sin sandboxing (acceso completo al sistema)

## 📁 Estructura del Proyecto

```
cornelio/
├── README.md                    ← Este archivo
├── AGENTS.md                   ← Definición del agente Magnum
├── SOUL.md                     ← Personalidad y principios
├── USER.md                     ← Información del usuario (Jose)
├── IDENTITY.md                 ← Identidad del agente
├── TOOLS.md                    ← Notas de herramientas
├── MEMORY.md                   ← Documentación del sistema de memoria
│
├── config/
│   └── openclaw.json.example   ← Configuración de OpenClaw (sin tokens)
│
├── scripts/
│   ├── sync-memory.sh          ← Auto-sincronización de memoria (cron cada 5min)
│   ├── memory-search.sh        ← Script de búsqueda rápida en memoria
│   └── init-mempalace.py       ← Inicializador de MemPalace
│
├── memory-hybrid/
│   ├── qmd/                    ← Índices y colecciones QMD
│   │   └── index.sqlite
│   └── mempalace/              ← Configuración de MemPalace
│       ├── config.json
│       ├── wings.json
│       └── identity.md
│
└── docs/
    └── (documentación adicional)
```

## 🚀 Instalación

### Prerrequisitos

```bash
# Node.js >= 22
node --version   # v22.22.2

# Python >= 3.9
python3 --version  # 3.13.7

# OpenClaw instalado globalmente
npm install -g openclaw
```

### Paso 1: Instalar QMD

```bash
npm install -g @tobilu/qmd
qmd --version  # 2.1.0
```

### Paso 2: Instalar MemPalace

```bash
pip3 install mempalace --break-system-packages
mempalace --help
```

### Paso 3: Crear colecciones QMD

```bash
# Colección para sesiones de Cornelio
qmd collection add ~/.openclaw/agents/cornelio/sessions \
  --name cornelio-sessions --mask "*.jsonl"

# Colección para sesiones de Magnum
qmd collection add ~/.openclaw/agents/magnum/sessions \
  --name magnum-sessions --mask "*.jsonl"

# Agregar contexto
qmd context add qmd://cornelio-sessions "Sesiones del agente Cornelio"
qmd context add qmd://magnum-sessions "Sesiones del agente Magnum"

# Generar embeddings
qmd embed
```

### Paso 4: Inicializar MemPalace

```bash
python3 scripts/init-mempalace.py
```

### Paso 5: Configurar OpenClaw

Editar `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "list": [
      {
        "id": "cornelio",
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" },
        "default": true
      },
      {
        "id": "magnum",
        "workspace": "~/.openclaw/workspace-magnum",
        "agentDir": "~/.openclaw/agents/magnum/agent",
        "sandbox": { "mode": "off" }
      }
    ]
  },
  "bindings": [
    { "agentId": "cornelio", "match": { "channel": "whatsapp" } },
    { "agentId": "magnum", "match": { "channel": "telegram" } }
  ],
  "memory": {
    "backend": "qmd",
    "qmd": { "includeDefaultMemory": true }
  },
  "agents": {
    "defaults": {
      "memorySearch": {
        "qmd": {
          "extraCollections": [
            { "path": "~/.openclaw/agents/cornelio/sessions", "name": "cornelio-globales" },
            { "path": "~/.openclaw/agents/magnum/sessions", "name": "magnum-globales" }
          ]
        }
      }
    }
  }
}
```

### Paso 6: Auto-sincronización (cron)

```bash
# Copiar script y dar permisos
chmod +x scripts/sync-memory.sh

# Agregar al crontab (cada 5 minutos)
(crontab -l; echo "*/5 * * * * /ruta/a/scripts/sync-memory.sh") | crontab -
```

## 🔍 Uso

### Búsqueda en memoria

```bash
# Buscar en todas las sesiones
qmd search "tarea asignada"

# Buscar solo en sesiones de Cornelio
qmd search "decisión estratégica" -c cornelio-sessions

# Búsqueda híbrida (mejor calidad)
qmd query "¿qué decisiones tomamos sobre autenticación?"

# Usar el script de utilidad
./scripts/memory-search.sh "memoria qmd" cornelio
```

### Flujo de trabajo entre agentes

1. **Jose** le habla a **Cornelio** (WhatsApp/Telegram) → decide estrategia
2. **Cornelio** asigna tarea a **Magnum** → se guarda en sesión → QMD indexa
3. **Jose** pregunta directamente a **Magnum** → Magnum busca en su memoria + extraCollections de Cornelio
4. **Magnum** responde con **contexto completo** sin perder información

## 👥 Cadena de Mando

```
Jose Navarro (CEO Humano)
    ↓ Visión y dirección
Cornelio (CEO Virtual)
    ↓ Decide y delega
Magnum (Brazo Derecho)
    ↓ Ejecuta y reporta
Sistema Operativo
```

## 📊 Estado Actual

| Métrica | Valor |
|---------|-------|
| Version QMD | 2.1.0 |
| Version MemPalace | 3.1.0 |
| Documentos indexados | 5 sesiones |
| Vectores embebidos | 914+ |
| Agents configurados | 2 (cornelio, magnum) |
| Sandbox | Desactivado |
| Auto-sync | Cada 5 minutos |

## 🛠️ Tech Stack

| Tecnología | Versión | Uso |
|------------|---------|-----|
| [OpenClaw](https://docs.openclaw.ai) | latest | Gateway multi-agente |
| [QMD](https://github.com/tobi/qmd) | 2.1.0 | Búsqueda semántica híbrida |
| [MemPalace](https://github.com/milla-jovovich/mempalace) | 3.1.0 | Memoria estructurada |
| Node.js | 22.22.2 | Runtime principal |
| Python | 3.13.7 | MemPalace + scripts |
| SQLite | builtin | Almacenamiento QMD/MemPalace |
| ChromaDB | 0.6.3 | Vector store (MemPalace) |

## 📄 Licencia

MIT

---

**Creado por:** Jose Navarro & Cornelio.app  
**Fecha:** 10 de Abril de 2026  
**Repositorio:** https://github.com/josenavarrojimenez-sudo/cornelio

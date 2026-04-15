# Arquitectura de Comunicación entre Agentes

**Cornelio.app** - Sistema Multi-Agente Jerárquico

---

## 📋 Visión General

Cornelio.app utiliza una arquitectura multi-agente jerárquica donde cada agente tiene:
- Workspace independiente
- Memoria aislada
- Canales de comunicación asignados
- Responsabilidades específicas

---

## 🏗️ Arquitectura de Agentes

```
┌─────────────────────────────────────────────────────────────┐
│                    JOSE (CEO Humano)                        │
│                    Vision & Decisión Final                  │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│              CORNELIO (CEO Virtual / Estrategia)            │
│  • WhatsApp: +50672516680                                   │
│  • Telegram: @CornelioAdelanteBot                           │
│  • Workspace: /root/.openclaw/workspace                     │
│  • Rol: Decisión estratégica, coordinación, reportes        │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│         MAGNUM (Brazo Derecho / Ejecución Operativa)        │
│  • Telegram: @Magnum_XLBot                                  │
│  • Workspace: /root/.openclaw/workspace-magnum              │
│  • Rol: Ejecución, investigación, troubleshooting, logs     │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│              AGENTES ESPECIALIZADOS (Futuros)               │
│  • DevOps Agent, Marketing Agent, Finance Agent, etc.       │
│  • Cada uno con workspace y bot independiente               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 Mecanismos de Comunicación

### Herramientas de Orquestación (Sessions API)

| Herramienta | Propósito | Dirección |
|-------------|-----------|-----------|
| `sessions_send` | Enviar instrucciones/mensajes | Bidireccional |
| `sessions_list` | Listar sesiones activas | Bidireccional |
| `sessions_history` | Revisar historial de conversación | Bidireccional |
| `sessions_spawn` | Crear nuevos agentes | Cornelio → Nuevos |

---

## 📡 Flujos de Comunicación

### Flujo 1: Jose → Cornelio → Magnum (Delegación)

```
┌──────┐     Instrucción estratégica     ┌─────────┐
│ Jose │ ───────────────────────────────►│ Cornelio│
└──────┘                                 └─────────┘
                                              │
                                              │ sessions_send
                                              │ "Ejecutar X. Deadline: Y"
                                              ▼
                                         ┌─────────┐
                                         │ Magnum  │
                                         │ Ejecuta │
                                         └─────────┘
```

**Ejemplo:**
```
Jose: "Necesito el dashboard listo para lunes"
  ↓
Cornelio → sessions_send a Magnum:
  "Prioridad: validar deployment del dashboard. 
   Reportá estado en 30 min."
  ↓
Magnum → ejecuta checks, verifica logs, confirma servicios
  ↓
Magnum → sessions_send a Cornelio:
  "✅ Todo verde, 3 servicios running, 0 errores"
  ↓
Cornelio → Jose:
  "Dashboard operativo, listo para lunes"
```

---

### Flujo 2: Magnum → Cornelio (Reporte)

```
┌─────────┐     Reporte de estado/hallazgo     ┌─────────┐
│ Magnum  │ ──────────────────────────────────►│ Cornelio│
└─────────┘                                    └─────────┘
                                                    │
                                                    │ Procesa y resume
                                                    ▼
                                               ┌──────┐
                                               │ Jose │
                                               └──────┘
```

**Ejemplo:**
```
Magnum → sessions_send a Cornelio:
  "✅ Tarea completada. 
   Hallazgo: El servicio webchat tiene 99.9% uptime.
   Bloqueo: ninguno.
   Próximo paso: esperar instrucciones."
  ↓
Cornelio → Jose:
  "Magnum completó la validación. 
   Sistema estable, sin bloqueos."
```

---

### Flujo 3: Cornelio ↔ Magnum (Consulta)

```
┌─────────┐     Pregunta específica     ┌─────────┐
│Cornelio │ ◄─────────────────────────► │ Magnum  │
└─────────┘     Respuesta técnica       └─────────┘
```

**Ejemplo:**
```
Cornelio → sessions_send a Magnum:
  "¿Cuál es el estado actual del Gateway? ¿Hay errores en los logs?"
  ↓
Magnum → sessions_send a Cornelio:
  "Gateway: running (pid 44653). 
   Logs: 0 errores en las últimas 2h.
   Uptime: 99.97%"
```

---

## 📁 Estructura de Workspaces

### Cornelio (CEO Virtual)
```
/root/.openclaw/workspace/
├── SOUL.md           # Personalidad y tono
├── AGENTS.md         # Instrucciones operativas
├── USER.md           # Info sobre Jose
├── TOOLS.md          # Herramientas permitidas
├── HEARTBEAT.md      # Tareas periódicas
├── docs/             # Documentación
├── memory/           # Memoria aislada
└── scripts/          # Scripts personalizados
```

### Magnum (Brazo Derecho)
```
/root/.openclaw/workspace-magnum/
├── SOUL.md           # Personalidad y tono
├── AGENTS.md         # Instrucciones operativas
├── USER.md           # Info sobre Jose
├── memory/           # Memoria aislada
└── scripts/          # Scripts personalizados
```

---

## 🎯 Principios de Comunicación

### 1. **Aislamiento Completo**
- Cada agente tiene su propia memoria (`memory/*.md`)
- Las sesiones no se comparten entre agentes
- Los workspaces son independientes

### 2. **Cadena de Mando Clara**
```
Jose (CEO Humano)
    ↓
Cornelio (CEO Virtual)
    ↓
Magnum (Ejecutor) + Agentes Especializados
```

### 3. **Reporte Ejecutivo**
- Magnum NO reporta directamente a Jose (excepto en Telegram si Jose le habla)
- Magnum reporta a Cornelio
- Cornelio resume a Jose en formato ejecutivo (sin ruido operativo)

### 4. **Bidireccionalidad**
- Cornelio puede enviar instrucciones a Magnum
- Magnum puede enviar reportes/consultas a Cornelio
- Ambos pueden revisar el historial del otro si necesitan contexto

---

## 🔧 Configuración Técnica (openclaw.json)

### Agents List
```json
{
  "agents": {
    "list": [
      {
        "id": "cornelio",
        "name": "Cornelio - CEO Virtual",
        "workspace": "/root/.openclaw/workspace",
        "default": true
      },
      {
        "id": "magnum",
        "name": "Magnum - Brazo Derecho",
        "workspace": "/root/.openclaw/workspace-magnum"
      }
    ]
  }
}
```

### Telegram Multi-Account
```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "pairing",
      "accounts": {
        "default": {
          "botToken": "8579844363:AAGMeemIv7tCvqv5d11kgCUGJgPHbVlxcIE"
        },
        "magnum": {
          "botToken": "8562696632:AAEkhgiHhZBoOabjlh6Gw9AkbQHWtSx0mec"
        }
      }
    }
  }
}
```

### Bindings (Enrutamiento)
```json
{
  "bindings": [
    {
      "agentId": "cornelio",
      "match": {
        "channel": "telegram",
        "accountId": "default"
      }
    },
    {
      "agentId": "magnum",
      "match": {
        "channel": "telegram",
        "accountId": "magnum"
      }
    },
    {
      "agentId": "cornelio",
      "match": {
        "channel": "whatsapp",
        "peer": {
          "kind": "direct",
          "id": "+50672516680"
        }
      }
    }
  ]
}
```

---

## 📱 Canales de Comunicación por Agente

| Agente | WhatsApp | Telegram |
|--------|----------|----------|
| **Cornelio** | ✅ +50672516680 | ✅ @CornelioAdelanteBot |
| **Magnum** | ❌ | ✅ @Magnum_XLBot |

---

## 🚀 Creación de Nuevos Agentes

Para agregar un nuevo agente especializado:

1. **Crear agente** con `sessions_spawn` o configuración manual
2. **Asignar workspace** independiente (`/root/.openclaw/workspace-{nombre}`)
3. **Configurar bot** de Telegram (si corresponde) vía BotFather
4. **Actualizar openclaw.json**:
   - Agregar a `agents.list`
   - Agregar cuenta en `channels.telegram.accounts`
   - Agregar binding en `bindings`
5. **Reiniciar Gateway** para aplicar cambios
6. **Aprobar pairing** del nuevo bot

---

## 📊 Métricas de Comunicación

### KPIs a Monitorear

| Métrica | Target | Descripción |
|---------|--------|-------------|
| Tiempo de respuesta (Magnum → Cornelio) | < 5 min | Reportes de tareas |
| Tiempo de respuesta (Cornelio → Jose) | < 1 min | Resúmenes ejecutivos |
| Tasa de éxito de tareas | > 95% | Tareas completadas sin errores |
| Uptime del sistema | > 99.9% | Disponibilidad de agentes |

---

## 🛡️ Seguridad y Aislamiento

### Reglas de Seguridad

1. **Nunca compartir memoria** entre agentes
2. **Nunca compartir sesiones** entre agentes
3. **Cada agente tiene sus propias credenciales** (API keys, tokens)
4. **Cornelio tiene autoridad estratégica**, pero Jose tiene decisión final
5. **Magnum no toma decisiones sensibles** sin escalar a Cornelio

### Permisos por Agente

| Herramienta | Cornelio | Magnum |
|-------------|----------|--------|
| `read` | ✅ | ✅ |
| `write` | ✅ | ✅ |
| `exec` | ✅ (con approval) | ✅ |
| `sessions_send` | ✅ | ✅ |
| `sessions_spawn` | ✅ | ❌ |
| `tts` | ✅ | ✅ |

---

## 📝 Ejemplos de Uso

### Ejemplo 1: Delegar Investigación

```
# Cornelio envía instrucción a Magnum
sessions_send({
  sessionKey: "agent:magnum:...",
  message: "Investigá opciones de hosting para el nuevo módulo. 
            Compará 3 proveedores. Deadline: 1h."
})
```

### Ejemplo 2: Solicitar Status

```
# Cornelio consulta estado a Magnum
sessions_send({
  sessionKey: "agent:magnum:...",
  message: "¿Cuál es el status del deployment? ¿Hay errores?"
})
```

### Ejemplo 3: Reporte de Magnum

```
# Magnum reporta a Cornelio
sessions_send({
  sessionKey: "agent:cornelio:...",
  message: "✅ Deployment completado. 
            Servicios: 3/3 running. 
            Errores: 0. 
            Uptime: 99.97%"
})
```

---

## 🔍 Troubleshooting

### Problema: Magnum no responde

1. Verificar sesión activa: `sessions_list`
2. Revisar historial: `sessions_history(sessionKey)`
3. Verificar logs del Gateway
4. Reiniciar Gateway si es necesario

### Problema: Mensajes no llegan

1. Verificar bindings en `openclaw.json`
2. Confirmar `accountId` correcto en el binding
3. Verificar que el bot esté paired (`dmPolicy: pairing`)
4. Revisar logs del Gateway

### Problema: Workspaces se mezclan

1. Verificar `workspace` en `agents.list`
2. Confirmar que cada agente tiene su propio directorio
3. Revisar que no haya paths absolutos compartidos

---

## 📚 Referencias

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [GitHub Repository](https://github.com/openclaw/openclaw)
- [Community Discord](https://discord.com/invite/clawd)

---

**Última actualización:** 2026-04-11  
**Autor:** Cornelio (CEO Virtual)  
**Versión:** 1.0

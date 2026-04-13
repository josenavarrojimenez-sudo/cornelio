# Backlog - Evaluar Después

Elementos guardados para revisión futura cuando Cornelio.app esté más consolidado.

##目录

- [2026-04-13](#2026-04-13)

---

## 2026-04-13

### AtlasCloud (n8n nodes)
**Link:** https://github.com/AtlasCloudAI/n8n-nodes-atlascloud

**Descripción:**
- Plataforma de inferencia AI (LLM, imagen, video)
- Nodos para n8n (automatización de workflows)
- API compatible con OpenAI
- Modelos: Claude, GPT, Gemini, generación imagen/video

**Costo:** Por verificar (potencialmente más barato que OpenAI/Anthropic)

**Potencial uso:**
- Generación de imágenes para Salonero Virtual (menús, etc.)
- Alternativa de inferencia para optimizar costos a largo plazo

**Estado:** 🔴 En espera
**Notas:** Muy nuevo (8 stars) — riesgo de soporte. Evaluar cuando tengamos volumen.

---

### Rescue Bot (Gateway Aislado)
**Descripción:**
- Crear un gateway separado (puerto 19001) solo para Cornelio
- Segundo bot de Telegram conectado al gateway rescue
- Si el gateway principal se cae, Jose puede seguir hablando con Cornelio
- Funciona como "bot de emergencia" cuando hay conflictos en el gateway principal

**Implementación:**
1. Crear segundo gateway con `--profile rescue`
2. Crear segundo bot de Telegram via @BotFather
3. Configurar Cornelio en el rescue gateway
4. Testear failover cuando el principal se caiga

**Para qué sirve:**
- Si hay conflicto y el gateway no levanta, Jose tiene forma de comunicarse conmigo
- Puedo帮他诊断 y arreglar el problema desde el rescue
- No queda completamente varado sin poder interactuar con los agentes

**Estado:** 🔴 En backlog
**Prioridad:** Alta (Jose lo pidió)
**Repositorio:** GitHub en carpeta `backlog/`

---

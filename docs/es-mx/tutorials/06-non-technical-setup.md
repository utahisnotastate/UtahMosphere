# Tutorial: Configuración sin tecnicismos

**Audiencia:** Usuarios no técnicos, dueños de pequeños negocios  
**Tiempo:** 20 minutos (con ayuda de alguien que sepa de tecnología)  
**Objetivo:** Poner UtahMosphere en marcha y desplegar tu primera aplicación

---

## ¿Qué es UtahMosphere?

Piensa en ello como un **cerebro de computadora pequeño** que ejecuta tu sitio web o aplicación **en tu oficina o casa** — sin factura mensual de nube de Amazon o Google.

Incluso **le puedes hablar**: "Deploy application my-store" y configura las cosas.

Guía completa en lenguaje sencillo: [Guía no técnica](../NON_TECHNICAL_GUIDE.md)

---

## Qué necesitas

| Artículo | Para qué |
|----------|----------|
| Mini PC o Raspberry Pi | El hardware "cerebro" |
| Internet (para configuración) | Descargar el software una vez |
| Un ayudante técnico (opcional) | Para el comando de instalación |
| Micrófono USB (opcional) | Para control por voz |

---

## Paso 1: Instala el cerebro

Tu ayudante ejecuta **un comando** en la Mini PC (Linux):

```bash
sudo bash setup.sh
```

Esto instala todo automáticamente. Toma unos 10–15 minutos.

**¿No tienes Linux?** Tu ayudante puede usar Docker en su lugar:

```bash
docker-compose up -d
```

---

## Paso 2: Verifica que funciona

Tu ayudante abre un navegador o terminal y verifica:

```bash
curl http://127.0.0.1:8999/health
```

Si ves `"healthy"` — el cerebro está despierto.

---

## Paso 3: Enséñale tu voz (opcional)

Tu ayudante ejecuta:

```bash
python voice_bridge.py
```

Di claramente: **"Claim node"**

Ahora solo tu voz (o un ayudante autorizado) puede controlar el sistema.

---

## Paso 4: Pon tu aplicación en línea

**Con voz:** Di **"Deploy application my-store"**

**Sin voz:** Tu ayudante ejecuta:

```bash
python examples/voice-deploy-simulator/deploy.py my-store
```

Eso es todo. Sin configuraciones complicadas de servidor.

---

## Paso 5: Ve qué está corriendo

Tu ayudante puede abrir el tablero verde:

```bash
python flux_gui.py
```

O verifica desde cualquier computadora en la misma red:

```bash
curl http://YOUR-MINI-PC-IP:8999/status
```

---

## Tareas del día a día (pídele a tu ayudante)

| Quieres… | Di o pide… |
|----------|------------|
| Agregar una app nueva | "Deploy application [nombre]" |
| Ver qué está corriendo | "Status grid" |
| Ver el tablero | Abrir la GUI Utah-Flux |
| Arreglar algo | Reiniciar: `sudo systemctl restart utahmosphere` |

---

## La promesa de "cero mantenimiento"

UtahMosphere limpia recursos viejos y se cura a sí mismo en segundo plano. Lo configuras una vez y sigue corriendo.

Para respaldo y recuperación, tu ayudante debe seguir: [Guía de desarrollo local](../LOCAL_DEVELOPMENT.md).

---

## Glosario

| Palabra | Significado sencillo |
|---------|----------------------|
| **Deploy** | Poner una app en el cerebro |
| **Claim node** | Enseñarle al cerebro tu voz |
| **Tenant** | Una app corriendo en el sistema |
| **Healthy** | El cerebro funciona bien |

Más ayuda: [Índice de recetas](../recipes/README.md)

# Tutorial: Tu primer mayordomo robot

**Audiencia:** Niños y familias  
**Tiempo:** 15 minutos  
**Necesitas:** Una computadora con UtahMosphere instalado, micrófono opcional

---

## Qué vas a construir

Un pequeño "Mayordomo Robot" en tu computadora que te escucha y despliega aplicaciones cuando se lo pides.

---

## Paso 1: Conoce al mayordomo

UtahMosphere es como tener un mayordomo robot en una cajita pequeña (Mini PC o Raspberry Pi). En lugar de pagarle a una empresa grande para alojar tus cosas, el mayordomo vive en **tu** cuarto.

Inicia el cerebro del mayordomo:

```bash
python utahmosphere_os.py
```

Pide ayuda a un adulto para configurar `UTAH_DATA_DIR` en una carpeta de tu computadora si no estás en Linux.

---

## Paso 2: Saluda al mayordomo

Abre una segunda ventana y ejecuta:

```bash
python voice_bridge.py
```

Cuando diga **"Listening..."**, intenta decir:

> **"Claim node"**

Esto le enseña al mayordomo tu voz. Es como darle una llave que solo tu voz puede usar.

---

## Paso 3: Construye un puesto de limonada

Di:

> **"Deploy application lemonade"**

El mayordomo crea una pequeña aplicación de "puesto de limonada" en la computadora. Verifica que funcionó:

```bash
curl http://127.0.0.1:8999/status
```

Busca `"lemonade"` en la lista de inquilinos.

---

## Paso 4: ¿Sin micrófono? ¡No hay problema!

Pide a un adulto que ejecute esto en su lugar:

```bash
python examples/voice-deploy-simulator/deploy.py lemonade
```

Mismo resultado — el mayordomo igual construye tu puesto.

---

## Paso 5: Mira la pantalla de control

Si tienes pantalla, ejecuta:

```bash
python flux_gui.py
```

Verás texto verde mostrando lo que hace el mayordomo — ¡como el tablero de una nave espacial!

---

## Lo que aprendiste

- **Claim node** = enseñarle al mayordomo tu voz
- **Deploy application** = construir algo nuevo
- El mayordomo guarda una lista de todo lo que construyó

---

## Retos divertidos

1. Despliega tres apps: `toys`, `games` y `art`
2. Di **"status grid"** y lee lo que reporta el mayordomo
3. Dibuja un retrato de tu Mayordomo Robot y etiqueta: Voz, Cerebro, Apps

Más actividades: [Índice de recetas](../recipes/README.md)

Guía para padres: [Explicación para niños](../ELI5_FOR_KIDS.md)

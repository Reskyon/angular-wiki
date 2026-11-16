# Navegación y movimiento: qué resuelve el navegador

Abre la portada en una ventana estrecha y elige «Experiencia» desde el menú. La dirección gana `#experience` y el título debe quedar visible debajo del encabezado. La parte que empieza en `#` se llama *fragmento*: señala un lugar dentro de la página.

## Caso resuelto: el encabezado tapa el título

Cuando un enlace lleva a una sección y su título desaparece debajo de la barra, compara la altura del encabezado con el espacio que deja el desplazamiento. En `HeaderComponent`, `ResizeObserver` informa cuando cambia el tamaño de la barra. Angular publica ese valor en `--header-height`, que CSS usa para el espacio superior. `provideFragmentScrolling` lee `scroll-padding-top` y aplica ese valor al desplazamiento de Angular. Así ambos usan la misma medida cuando la barra se vuelve más alta.

**Dónde empiezo.** Desde la portada y en vista móvil, elijo Experiencia desde el menú. Si `#experience` no aparece en la URL, reviso el enlace. Si aparece y el título queda tapado, el enlace llegó a la sección y puedo aislar el cálculo del desplazamiento.

1. En **Elementos**, selecciono `<html>` y comparo `--header-height` con la altura real de la barra. Si la medida no se actualiza al ampliar el texto, miro `ResizeObserver` en `HeaderComponent`.
2. Si la medida es correcta, miro el valor calculado de `scroll-padding-top`. Si CSS ya deja el espacio esperado pero la navegación de Angular sigue tapando el título, reviso `setOffset` en `provideFragmentScrolling`. Angular consulta ese valor al desplazarse.
3. Vuelvo a seleccionar la sección desde el menú con el texto ampliado. La prueba es que el título queda visible bajo la barra. En escritorio, donde la barra deja de estar fija, no debe quedar el espacio sobrante de móvil.

Cambiar de idioma es una comprobación distinta. `LanguageSwitcherComponent` cambia el primer segmento de la URL y conserva el resto, incluido `#experience`. En una portada ya desplazada, las etiquetas cambian y el lector se mantiene en el mismo lugar. Si en ese caso vuelve a saltar al título, reviso `KEEP_SCROLL` en el selector antes de tocar la altura del encabezado.

La guía DIY (`/en/diy`) es la excepción a propósito. Mientras lees, la URL guarda el paso en el fragmento (`#styles`, por ejemplo) sin mover la página. Al cambiar de idioma, el selector conserva ese fragmento y la otra versión baja hasta el mismo paso, porque los dos idiomas no miden lo mismo. Si llegas arriba de la página en lugar de al paso, mira primero si la URL tenía el fragmento antes de cambiar de idioma; si lo tenía, revisa `scrollInfoFor` en el selector. [Cómo se construyó la guía](07-guia-diy.md#módulo-d3-la-url-que-sigue-el-paso-y-el-cambio-de-idioma).

Encabezado · Desplazamiento por fragmento

## Caso resuelto: aparece movimiento al recargar con el interruptor apagado

Apaga las animaciones y recarga. El navegador ya tiene la preferencia en `localStorage`. Un script pequeño en `src/index.html` la aplica a `<html>` antes de que Angular arranque, para evitar un destello de movimiento. Cuando Angular arranca, `MotionService` usa esa misma preferencia para sincronizar el interruptor y el comportamiento de la aplicación.

**Dónde empiezo.** Con el interruptor apagado, compruebo en el almacenamiento local del navegador si `motion` tiene el valor `off`. Luego recargo la misma página y observo si el efecto aparece solo al principio o sigue después de que Angular arranca.

| Lo que veo | Qué reviso primero |
| --- | --- |
| Apagar el interruptor funciona, pero `motion` no queda guardado. | `MotionService.store()` y si el navegador permite usar almacenamiento local. El cambio puede funcionar durante la visita aunque la preferencia no se conserve. |
| `motion` queda en `off` y se ve un destello al recargar. | El HTML de la respuesta y el script en `src/index.html`. El atributo `data-motion="off"` debe aplicarse al inicio, antes de que Angular se sincronice con la preferencia. Ver el atributo después de cargar la página no basta para comprobar el primer instante. |
| Ya aparece `data-motion="off"`, pero un efecto sigue activo. | Sigo ese efecto. CSS lee el atributo, mientras las animaciones controladas por Angular siguen el estado de `MotionService`. |

La señal completa es que al recargar no se ve un destello, el interruptor sigue apagado y se puede activar de nuevo sin recargar. El HTML generado incluye el script temprano. La preferencia de cada visitante se lee al abrirlo en su navegador.

Script anterior al arranque · [Guía de animaciones](04-animaciones.md) · [Guía del desplazamiento y el encabezado](03-secciones-de-portify.md)

**Siguiente capítulo:** [Compilación y publicación](learn-release.md).

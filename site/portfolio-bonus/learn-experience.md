# Experiencia: sigue un dato desde el YAML hasta la página

Abre [Experiencia en español](https://janioisacura.com/es/#experience). Busca la entrada de Reskyon y la palabra «Actualidad». La primera viene del archivo de contenido. La segunda es una etiqueta de la interfaz para los trabajos que siguen en curso. Esta distinción ayuda a elegir dónde empezar por cualquier cambio de texto.

## Del texto visible al archivo

1. Abre `content/es/experience.yml` y busca `id: reskyon`. Ahí están `organization`, `role`, `startDate` y `highlights`. El identificador `id` sirve para reconocer la entrada aunque su texto cambie. La versión inglesa está en `content/en/experience.yml`.
2. En `scripts/prepare-content.mjs`, busca `validateExperience`. Recibe los valores leídos del YAML y comprueba qué campos existen y qué valores admiten. Más abajo, `writeLocalized` escribe `src/app/home/generated/experience.ts`. Este archivo se vuelve a escribir al preparar contenido. Si quieres modificar un dato de origen, empieza en el YAML.
3. En `experience.component.ts`, `EXPERIENCE[this.locale()]` selecciona la lista del idioma que recibe el componente. Abre `experience.component.html` en la misma carpeta: `@for` dibuja la lista y `track item.id` permite a Angular reconocer cada entrada. La plantilla muestra la fecha final cuando existe y usa la etiqueta «Actualidad» en español cuando falta.
4. `npm run build` prepara los datos y luego pide a Angular que genere el HTML. Busca el texto en `dist/janioisacura/browser/es/index.html`. La compilación ya lo incluyó en el documento que recibirá el navegador.

Contenido de Experiencia en español · Validador y generación · Componente y plantilla

## Caso resuelto: mostrar la modalidad de trabajo

Imagina que la ficha de Reskyon debe mostrar «Remoto» junto a la organización. El campo `location` de este ejemplo sería una ampliación de la app publicada.

1. Añadimos `location: Remoto` a Reskyon en el YAML español y `location: Remote` en el inglés. Al ejecutar `npm run content:prepare`, el validador original rechaza `location` como campo desconocido. Ya sabemos en qué capa está el bloqueo.
2. En `validateExperience`, agregamos `'location'` a `fields` y usamos la función `isText` que ya utiliza el validador. Si el campo falta, la entrada sigue siendo válida. Si está presente, debe contener texto.

   ```js
   if (item.location !== undefined && !isText(item.location)) {
     fail(`${label}: "location" must be a non-empty string.`)
   }
   ```

3. En `src/app/home/interfaces/experience.interface.ts` agregamos `location?: string`. El signo `?` significa que la propiedad puede faltar. El tipo ayuda a Angular a trabajar con el dato. La validación anterior sigue siendo necesaria porque el YAML se lee fuera de TypeScript.
4. En `experience.component.html`, el separador va dentro del mismo `@if` que el texto. Tras regenerar, Reskyon mostraría «Remoto» en español y «Remote» en inglés. ZS seguiría sin separador.

   ```html
   <p class="organization">
     {{ item.organization }}
     @if (item.location) {
       <span> · {{ item.location }}</span>
     }
   </p>
   ```
5. La comprobación tiene dos capas. En `scripts/prepare-content.test.mjs`, una prueba con `{ ...entry, location: 'Remote' }` debe pasar y otra con `{ ...entry, location: '' }` debe fallar por `location`. En el navegador y en el HTML compilado comprobamos la presentación. Cada comprobación responde una pregunta distinta.

Si el servidor de desarrollo ya está abierto, `npm run content:prepare` regenera los datos. Si el texto aparece en el módulo generado pero falta en la página, la siguiente parada es la plantilla.

## Caso resuelto: el contenido falla por una fecha

En la versión inglesa, GlobalLogic es la tercera entrada y comienza en `'2021-08'`. Si en una copia de práctica cambiamos su fecha final a `'2021-07'`, `npm run content:prepare` señalará el archivo `content/en/experience.yml`, la entrada 3 y la regla que impide terminar antes de empezar. La entrada 3 es la tercera posición de la lista.

En `validateExperience` aparecen dos comprobaciones consecutivas. Primero revisa el formato `YYYY-MM`. A continuación compara las dos fechas. `'2021-07'` pasa el formato y falla por el orden. En cambio, `'2025-1'` falla por el formato, antes de que el script compare nada. Con cuatro dígitos de año y dos de mes, el orden de las cadenas coincide con el orden cronológico.

La solución del caso es restaurar la fecha real, `'2025-01'`, y volver a ejecutar la preparación. Así se verifica la corrección en la capa que informó el error. La misma validación corre antes de compilar con `npm run build`.

## Caso resuelto: dos idiomas con el mismo orden

Hoy se valida cada lista por separado. Si ZS y GlobalLogic se intercambian solo en español, la preparación puede pasar y las dos páginas mostrarán un orden distinto. Este caso enseña cómo añadir **una regla de ejemplo**, que no forma parte del comportamiento publicado.

1. Definimos la regla: los `id` deben coincidir por posición. Los roles y las descripciones pueden traducirse. Vamos a usar inglés como referencia.
2. En `scripts/prepare-content.test.mjs` se puede probar una función vacía llamada `checkSameExperience`. Con `assert.doesNotThrow`, dos listas iguales deben pasar. Con `assert.throws`, dos listas reordenadas o una lista incompleta deben fallar. Con la función vacía, estas últimas pruebas fallan porque esperaban una excepción que nunca llegó.
3. La función recorre la longitud de la lista más larga. Así también alcanza el punto donde falta o sobra una entrada.

   ```js
   export function checkSameExperience({ en, es }) {
     for (let index = 0; index < Math.max(en.length, es.length); index++) {
       const expected = en[index]?.id
       const actual = es[index]?.id
       if (expected !== actual) {
         throw new Error(
           `content/es/experience.yml: entry ${index + 1}: expected id "${expected ?? '<none>'}", found "${actual ?? '<missing>'}".`,
         )
       }
     }
   }
   ```

4. En `prepareContent`, llamamos a `checkSameExperience(experience)` después del bucle de los idiomas, cuando ambas listas están disponibles, y antes de generar los módulos. Una prueba directa con `node --test scripts/prepare-content.test.mjs` verifica la regla. Para comprobar la conexión, intercambiamos otra vez ZS y GlobalLogic solo en español: ahora `npm run content:prepare` debe señalar dónde difieren. Restauramos el orden y la preparación vuelve a pasar.

Una de las pruebas quedaría así. El ejemplo usa el `assert` y el `test` que el archivo ya importa, y añade `checkSameExperience` a la lista de funciones importadas desde `prepare-content.mjs`.

```js
test('reports the first experience missing from Spanish', () => {
  const en = [{ id: 'zs' }, { id: 'globallogic' }]
  const es = [{ id: 'zs' }]

  assert.throws(
    () => checkSameExperience({ en, es }),
    /entry 2: expected id "globallogic", found "<missing>"/,
  )
})
```

La secuencia explica una forma de trabajar fácil de mostrar en una presentación: primero observamos el comportamiento, luego definimos el nuevo requisito y finalmente comprobamos que se aplica al flujo real.

**Siguiente capítulo:** [Proyectos: del Markdown a una URL](learn-projects.md). Para ver el formato de las fechas y el resto de la sección, consulta el [módulo de Experiencia de la guía de construcción](03-secciones-de-portify.md).

# novedades-profes-ja

[Bot de Telegram][1] para recibir las últimas noticias publicadas en las secciones de [novedades del profesorado][2] y [novedades en centros][3], de la página web de la Consejería de Educación de la Junta de Andalucía.

## Creación del archivo `config.json`

Clonamos el repositorio:

```bash
git clone https://github.com/josejuansanchez/novedades-profes-ja.git
```

Accedemos la directorio del proyecto:

```bash
cd novedades-profes-ja
```

Creamos un nuevo archivo de configuración con el nombre `config.json` a partir del  archivo de ejemplo `config.example.json`:

```bash
cp config.example.json config.json
```

## Configuración del archivo `config.json`

Una vez que hemos creado el archivo `config.json` tenemos que configurar los parámetros de nuestro bot.

* `bot-token`: Es el token que Telegram nos devuelve al crear nuestro bot.
* `database`: Es la ruta y el nombre de nuestra base de datos sqlite.
* `urls`: Es la lista de urls con los feeds RSS que queremos parsear.

```JSON
{
    "bot-token" : "PUT-YOUR-TELEGRAM-BOT-TOKEN-HERE",

    "database" : "data/novedades.sqlite",
    
    "urls" : [
        "http://www.juntadeandalucia.es/educacion/portals/delegate/rss/ced/portalconsejeria/profesorado/-/-/true/OR/_self/ishare_noticefrom/DESC/",
        "http://www.juntadeandalucia.es/educacion/portals/delegate/rss/ced/portalconsejeria/centro-1/-/-/true/OR/true/cm_modified/DESC/"
    ]
}
```

## Creación de un entorno virtual con `virtualenv`

Instalamos `virtualenv` vía `pip`:

```bash
pip install virtualenv
```

Comprobamos que se ha instalado correctamente:

```bash
virtualenv --version
```

Creamos un entorno virtual para nuestro proyecto:

```bash
virtualenv my_virtualenv
```

Instalamos los paquetes necesarios para trabajar con nuestro proyecto. La lista de paquetes está definida en el archivo `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

Para poder usar nuestro entorno virtual es necesario activarlo:

```bash
source my_virtualenv/bin/activate
```

Para desactivar el entorno virtual ejecutaremos:

```bash
deactivate
```

## Parseo de feeds RSS y ejecución el bot

Para poder parsear los feeds RSS y guardar los datos en la base de datos ejecutaremos:

```bash
(my_virtualenv)$  python3 rss.py
```

Para ejecutar el bot:

```bash
(my_virtualenv)$  python3 bot.py
```


## Referencias

* [Bots: An introduction for developers][1].

## Librarías utilizadas en este proyecto

* [`python-telegram-bot`][4].

## Créditos

Este bot ha sido desarrollado por [José Juan Sánchez][5].

## Licencia

```
Copyright 2017 José Juan Sánchez

Licensed under the GNU General Public License, Version 3 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.gnu.org/licenses/gpl-3.0.en.html

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```


[1]: https://core.telegram.org/bots
[2]: http://www.juntadeandalucia.es/educacion/portals/web/ced/profesorado
[3]: http://www.juntadeandalucia.es/educacion/portals/web/ced/centros
[4]: https://github.com/python-telegram-bot/python-telegram-bot
[5]: http://josejuansanchez.org
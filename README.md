# novedades_educacion_andalucia

[Bot de Telegram][1] para recibir las últimas noticias publicadas en la página web de la [Consejería de Educación de la Junta de Andalucía][2].

## Creación del archivo `config.json`

Clonamos el repositorio:

```bash
git clone https://github.com/josejuansanchez/novedades-educacion-andalucia.git
```

Accedemos al directorio `educabot`:

```bash
cd novedades-educacion-andalucia/educabot/config
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

    "database_path" : "database/educabot.sqlite",

    "sources" : [
        {
            "name" : "Alumnado",
            "url" : "http://www.juntadeandalucia.es/educacion/portals/delegate/rss/ced/portalconsejeria/alumnado/-/-/true/AND/true/ishare_noticefrom/DESC/"
        },
        {
            "name" : "Profesorado",
            "url" : "http://www.juntadeandalucia.es/educacion/portals/delegate/rss/ced/portalconsejeria/profesorado/-/-/true/OR/_self/ishare_noticefrom/DESC/"
        },
        {
            "name" : "Familias",
            "url" : "http://www.juntadeandalucia.es/educacion/portals/delegate/rss/ced/portalconsejeria/familia/-/-/true/AND/false/ishare_noticefrom/DESC/"
        },
        {
            "name" : "Centros",
            "url" : "http://www.juntadeandalucia.es/educacion/portals/delegate/rss/ced/portalconsejeria/centro-1/-/-/true/OR/true/cm_modified/DESC/"
        }
    ]
}
```

## Instalación de un entorno virtual con `virtualenv`

Instalamos `virtualenv` con `pip3`:

```bash
pip3 install virtualenv
```

Comprobamos que se ha instalado correctamente:

```bash
virtualenv --version
```

## Creación de un entorno virtual con `virtualenv`

Creamos un entorno virtual para nuestro proyecto:

```bash
virtualenv my_virtualenv
```

Para poder usar nuestro entorno virtual es necesario activarlo:

```bash
source my_virtualenv/bin/activate
```

Para desactivar el entorno virtual ejecutaremos:

```bash
deactivate
```

## Instalación de dependencias

Instalamos los paquetes necesarios para trabajar con nuestro proyecto. La lista de paquetes está definida en el archivo `requirements.txt`:

```bash
(my_virtualenv)$ pip3 install -r requirements.txt
```

## Ejecución el bot

Para iniciar el bot ejecutaremos:

```bash
(my_virtualenv)$ python3 bot.py
```

## Cómo desplegar el bot en Heroku

Instalaremos [Heroku CLI][7] para poder crear y administrar aplicaciones en [Heroku][6] desde la línea de comandos.

El archivo `runtime.txt` contiene la versión de python con la que se ejecutará nuestro bot.

```
python-3.6.3
```

El archivo `Procfile` contiene el comando que se ejecutará en [Heroku][6] para iniciar el bot.

```
bot: cd educabot && python3 bot-heroku.py
```

El archivo `bot-heroku.py` contiene el código del bot que desplegaremos en Heroku. En este archivo el token de Telegram se gestiona con una variable de entorno del sistema. En nuestro caso será la variable `BOT_TOKEN`.

```python
self.updater = Updater(os.environ['BOT_TOKEN'])
```


## Referencias

* [Bots: An introduction for developers][1].

## Créditos

* [`python-telegram-bot`][3].
* [RobotRSS - A Telegram RSS Bot][5].

## Créditos

Este bot ha sido desarrollado por [José Juan Sánchez][4].

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
[2]: http://www.juntadeandalucia.es/educacion/portals/web/ced
[3]: https://github.com/python-telegram-bot/python-telegram-bot
[4]: http://josejuansanchez.org
[5]: https://github.com/cbrgm/telegram-robot-rss/
[6]: https://www.heroku.com
[7]: https://devcenter.heroku.com/articles/heroku-cli
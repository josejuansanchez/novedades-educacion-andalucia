# EducaBot - Bot de Telegram

[Bot de Telegram][1] para recibir las últimas noticias publicadas en la página web de la [Consejería de Educación de la Junta de Andalucía][2].

## Índice de contenidos

* `bot.py`
  * [Creación del archivo `config.json`](#creación-del-archivo-configjson)
  * [Configuración del archivo `config.json`](#configuración-del-archivo-configjson)
  * [Instalación de un entorno virtual con `virtualenv`](#instalación-de-un-entorno-virtual-con-virtualenv)
  * [Creación de un entorno virtual con `virtualenv`](#creación-de-un-entorno-virtual-con-virtualenv)
  * [Instalación de dependencias](#instalación-de-dependencias)
  * [Ejecución el bot](#ejecución-el-bot)
* `bot-heroku.py`
  * [Requisitos para desplegar el bot en Heroku](#requisitos-para-desplegar-el-bot-en-heroku)
  * [Cómo desplegar el bot en Heroku](#cómo-desplegar-el-bot-en-heroku)
* [Referencias](#referencias)
* [Créditos](#créditos)

## Creación del archivo `config.json`

Clonamos el repositorio:

```bash
git clone https://github.com/josejuansanchez/novedades-educacion-andalucia.git
```

Accedemos al directorio `config`:

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

## Requisitos para desplegar el bot en Heroku

Instalaremos [Heroku CLI][7] para poder crear y administrar aplicaciones en [Heroku][6] desde la línea de comandos.

También vamos a necesitar dos archivos especiales: [`runtime.txt`](runtime.txt) y [`Procfile`](Procfile).

* El archivo [`runtime.txt`](runtime.txt) contiene la versión de python con la que se ejecutará nuestro bot.

```
python-3.6.4
```

* El archivo [`Procfile`](Procfile) contiene el comando que se ejecutará en [Heroku][6] para iniciar el bot.

```
bot: cd educabot && python3 bot-heroku.py
```

El archivo [`bot-heroku.py`](educabot/bot-heroku.py) contiene el código del bot que desplegaremos en Heroku. En este archivo el token de Telegram se gestiona con una variable de entorno del sistema. En nuestro caso será la variable `BOT_TOKEN`.

```python
self.updater = Updater(os.environ['BOT_TOKEN'])
```

Esta variable se puede configurar desde la línea de comandos con las utilidades que hemos instalado con [Heroku CLI][7] o también se puede configurar desde el panel de control web donde administramos nuestras aplicaciones en [Heroku][6].

Por ejemplo, desde la línea de comandos con [Heroku CLI][7] ejecutaríamos:

```bash
heroku config:set BOT_TOKEN=123456789:AAABBBCCCDDDEEEFFFGGGHHHIIIJJJKKKLL
```

## Cómo desplegar el bot en Heroku

La secuencia de comandos que habría que ejecutar para desplegar el bot en [Heroku][6] es la siguiente:

```bash
heroku login
heroku create --region eu novedades-educacion-bot
git push heroku master
heroku config:set BOT_TOKEN=123456789:AAABBBCCCDDDEEEFFFGGGHHHIIIJJJKKKLL
heroku ps:scale bot=1
```

Para consultar el archivo de log podemos usar:

```bash
heroku logs --tail
```

Para detener la ejecución del bot usamos:

```bash
heroku ps:stop bot
```

Puedes encontrar más información sobre cómo desplegar con Git en Heroku en la [documentación oficial][10].

## Referencias

* [Bots: An introduction for developers][1].
* [Hosting telegram bot on Heroku for free][8].
* [Polling vs WebHooks in Telegram Bots][9].

## Créditos

Se han utilizado los siguientes ejemplos y librerías:

* [`python-telegram-bot`][3].
* [RobotRSS - A Telegram RSS Bot][5].

## Autor

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
[8]: https://github.com/Kylmakalle/heroku-telegram-bot
[9]: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
[10]: https://devcenter.heroku.com/articles/git

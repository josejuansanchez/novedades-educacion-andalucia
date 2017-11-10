# novedades-profes-ja

[Bot de Telegram][1] para recibir las últimas noticias publicadas en las secciones de [novedades del profesorado][2] y [novedades en centros][3], de la página web de la Consejería de Educación de la Junta de Andalucía.

## Primeros pasos

Clonamos el repositorio:

```bash
git clone https://github.com/josejuansanchez/novedades-profes-ja.git
```

Accedemos la directorio del proyecto:

```bash
cd novedades-profes-ja
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

Para desactivarlo ejecutaremos:

```bash
deactivate
```

## Referencias

* [Bots: An introduction for developers][1].
* [`python-telegram-bot`][4].


[1]: https://core.telegram.org/bots
[2]: http://www.juntadeandalucia.es/educacion/portals/web/ced/profesorado
[3]: http://www.juntadeandalucia.es/educacion/portals/web/ced/centros
[4]: https://github.com/python-telegram-bot/python-telegram-bot
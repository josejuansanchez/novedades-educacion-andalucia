# novedades-profes-ja
Novedades para los profesores de la Junta de Andalucía


## Primeros pasos

Clonamos el repositorio en nuetro equipo:

```bash
git clone https://github.com/josejuansanchez/novedades-profes-ja.git
```

Accedemos la directorio del proyecto:

```bash
cd novedades-profes-ja
```

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

Para desactivarlo ejecuaremos:

```bash
deactivate
```
## Web Scrapping para encontrar electivas virtuales en la UNAL
Para que **Selenium** funcione adecuadamente, es necesario el *driver* del navegador correspondiente (en este caso **Chrome** por facilidad), la página [Selenium with Python](https://selenium-python.readthedocs.io/) da una buena idea sobre la instalación.

Importante escribir las credenciales de la cuenta institucional en el archivo *credentials* de la forma:
```sh
username:<nombre de usuario sin @unal.edu.co>
password:<contrasena de la cuenta>
```
 
**Tener en cuenta**: Los elementos del SIA cambian sus atributos (ids, clases, nombres) en algunas ocasiones, es por eso que muchos se encuentran mejor con un selector de CSS.


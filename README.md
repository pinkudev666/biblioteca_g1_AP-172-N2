# Sistema de Biblioteca — Proyecto AP-172-N2

Desarrollo en Python para la gestión de préstamos de libros físicos en una biblioteca universitaria.  
Implementa una arquitectura modular en capas (CLI / Negocio / Datos) y permite registrar usuarios, gestionar libros y controlar préstamos.

---

## 🧩 Contexto del proyecto

La **biblioteca de una universidad** desea informatizar su sistema de préstamos de libros físicos.  
El sistema permite registrar usuarios, gestionar libros y registrar tanto préstamos como devoluciones con fechas y estados actualizados.

---

## ⚙️ Requerimientos funcionales

- Registrar **usuarios** (estudiantes y profesores)
- Gestionar **libros** con sus datos y estado (*disponible* o *prestado*)
- Realizar **préstamos y devoluciones** con fechas registradas
- Generar **reportes de préstamos vencidos**

---

## 🎭 Casos de uso

1. Un **estudiante** solicita un libro disponible → se genera el préstamo.  
2. Un **profesor** devuelve un libro fuera de plazo → el sistema marca el préstamo como **retrasado**.

---

## 🚀 Ejecución del programa

Asegúrate de ejecutar desde la **raíz del proyecto**:

```bash
python main.py
```

---

## 🧩 Módulos del Proyecto

### 1. `auxiliares`
Reúne funciones y clases de uso general que sirven de apoyo al resto del sistema.
Incluye herramientas para validación de datos, formateo de fechas, operaciones con cadenas y otras utilidades que facilitan el mantenimiento del código.
**Propósito:** evitar la duplicación de lógica común y mantener un código más limpio y reutilizable.  

---

### 2. `datos`
Maneja todo lo relacionado con la persistencia de la información.
Aquí se implementan los métodos para leer y escribir archivos, conectarse a bases de datos o interactuar con fuentes externas.
**Propósito:** separar la gestión de datos del resto del sistema, de modo que los cambios en el almacenamiento no afecten la lógica principal.

---

### 3. `negocio`
Contiene las reglas de negocio que definen el comportamiento central de la aplicación.
Es el módulo que coordina la lógica entre los datos y la interfaz, aplicando cálculos, validaciones y procesos clave.
**Propósito:** mantener organizada la parte funcional del sistema y asegurar que todas las operaciones sigan las normas del dominio.

---

### 4. `modelos`
Define las entidades del dominio, como clases que representan objetos del sistema (por ejemplo: Usuario, Libro, Préstamo).
Cada modelo agrupa sus atributos y métodos, facilitando la comunicación entre la lógica de negocio y la capa de datos.
**Propósito:** ofrecer una representación clara y estructurada de los elementos principales del programa.

---

### 5. `iu` (Interfaz de Usuario)
  
**Objetivo:** Administra la interacción con el usuario, principalmente mediante menús en consola.
Recibe las acciones del usuario y las comunica al módulo de negocio, mostrando los resultados correspondientes.
**Propósito:** mantener separada la lógica de presentación de la lógica interna, favoreciendo la modularidad y la facilidad de mantenimiento.

---

## 📦 Instalación de dependencias

Para ejecutar la instalación de todas las dependencias definidas para el proyecto, crea un archivo llamado requirements.txt en la raíz del repositorio.

Luego, desde la terminal, navega hasta el directorio donde se encuentra el archivo y ejecuta:

```bash
pip install -r requirements.txt
```

## 📂 Ejemplo de requirements.txt

El contenido del archivo debe incluir únicamente las librerías utilizadas en el proyecto:

```bash
mysql-connector-python
prettytable
SQLAlchemy
```

## 👩‍💻 Autores

- Paula Contreras (@pinkudev666)
- Diego Elgueta (@N4-g1)

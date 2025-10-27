CREATE DATABASE IF NOT EXISTS biblioteca_db;
USE biblioteca_db;

-- TABLA: Tipo_usuario
CREATE TABLE IF NOT EXISTS Tipo_usuario (
    id_tipo_usuario INT AUTO_INCREMENT PRIMARY KEY,
    tipo_usuario VARCHAR(50) NOT NULL
);


-- TABLA: Usuario
CREATE TABLE IF NOT EXISTS Usuario (
    rut_usuario VARCHAR(15) PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    correo_usuario VARCHAR(100) NOT NULL UNIQUE,
    id_tipo_usuario INT NOT NULL,
    FOREIGN KEY (id_tipo_usuario) REFERENCES Tipo_usuario(id_tipo_usuario)
);


-- TABLA: Libro
CREATE TABLE IF NOT EXISTS Libro (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    isbn_libro VARCHAR(20) NOT NULL UNIQUE,
    nombre_libro VARCHAR(150) NOT NULL,
    autor_libro VARCHAR(100) NOT NULL,
    copias_disponibles INT DEFAULT 0
);


-- TABLA: Prestamo
CREATE TABLE IF NOT EXISTS Prestamo (
    id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
    fecha_inicio DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    rut_usuario VARCHAR(15) NOT NULL,
    id_libro INT NOT NULL,
    estado ENUM('Pendiente', 'Devuelto a tiempo', 'Devuelto atrasado') NOT NULL DEFAULT 'Pendiente',
    FOREIGN KEY (rut_usuario) REFERENCES Usuario(rut_usuario),
    FOREIGN KEY (id_libro) REFERENCES Libro(id_libro)
);


-- TABLA: Multa
CREATE TABLE IF NOT EXISTS Multa (
    id_multa INT AUTO_INCREMENT PRIMARY KEY,
    monto_multa DECIMAL(6,2) NOT NULL,
    fecha_generacion DATE NOT NULL DEFAULT CURRENT_DATE,
    id_prestamo INT NOT NULL,
    FOREIGN KEY (id_prestamo) REFERENCES Prestamo(id_prestamo)
);


-- TABLA: Notificacion
CREATE TABLE IF NOT EXISTS Notificacion (
    id_notificacion INT AUTO_INCREMENT PRIMARY KEY,
    mensaje_notificacion VARCHAR(255) NOT NULL,
    fecha_envio DATE NOT NULL DEFAULT CURRENT_DATE,
    id_prestamo INT NOT NULL,
    FOREIGN KEY (id_prestamo) REFERENCES Prestamo(id_prestamo)
);



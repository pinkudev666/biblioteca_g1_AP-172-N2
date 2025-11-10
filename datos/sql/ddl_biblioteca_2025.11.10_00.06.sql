-- Para la tabla Libro
ALTER TABLE libro
ADD COLUMN activo TINYINT(1) NOT NULL DEFAULT 1;

-- Para la tabla Tipo_usuario
ALTER TABLE tipo_usuario
ADD COLUMN activo TINYINT(1) NOT NULL DEFAULT 1;

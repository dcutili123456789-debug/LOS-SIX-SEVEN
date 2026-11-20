USE gestion_tercera_edad;

CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario    VARCHAR(50) NOT NULL UNIQUE,
    contrasena CHAR(64) NOT NULL
);

ALTER TABLE Residente
    ADD COLUMN ci VARCHAR(20) NOT NULL UNIQUE AFTER id_residente,
    ADD COLUMN apellidos VARCHAR(80) NOT NULL AFTER nombre,
    ADD COLUMN sexo ENUM('Femenino','Masculino') NOT NULL AFTER fecha_nac,
    ADD COLUMN fecha_ingreso DATE NOT NULL AFTER sexo,
    ADD COLUMN contacto_familiar VARCHAR(150) NULL AFTER fecha_ingreso;

ALTER TABLE Historial
    ADD COLUMN responsable VARCHAR(100) NOT NULL AFTER fecha;

ALTER TABLE Prescripcion
    ADD COLUMN id_historial INT NULL AFTER id_prescripcion,
    ADD COLUMN frecuencia VARCHAR(80) NOT NULL AFTER dosis,
    ADD CONSTRAINT fk_prescripcion_historial
        FOREIGN KEY (id_historial) REFERENCES Historial(id_historial);

ALTER TABLE Categoria
    ADD CONSTRAINT uq_categoria_nombre UNIQUE (nombre);

ALTER TABLE Proveedor
    ADD CONSTRAINT uq_proveedor_nombre UNIQUE (nombre);

ALTER TABLE Insumo
    ADD COLUMN descripcion VARCHAR(200) NULL AFTER nombre;

ALTER TABLE Medicamento
    MODIFY principio_activo VARCHAR(100) NULL;

ALTER TABLE Lote
    ADD COLUMN numero_lote VARCHAR(50) NOT NULL AFTER id_proveedor,
    ADD CONSTRAINT uq_lote_insumo_numero UNIQUE (id_insumo, numero_lote),
    ADD CONSTRAINT chk_lote_cantidad CHECK (cantidad >= 0);

ALTER TABLE Movimiento
    ADD COLUMN observacion VARCHAR(200) NULL AFTER fecha,
    ADD CONSTRAINT chk_movimiento_cantidad CHECK (cantidad > 0);

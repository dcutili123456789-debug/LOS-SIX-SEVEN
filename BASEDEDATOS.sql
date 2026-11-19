DROP DATABASE IF EXISTS gestion_tercera_edad;
CREATE DATABASE gestion_tercera_edad
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE gestion_tercera_edad;

CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,            -- aqui se guarda el hash, no la clave
    rol ENUM('administrador', 'enfermeria', 'almacen', 'cuidador') NOT NULL,
    estado ENUM('activo', 'inactivo') NOT NULL DEFAULT 'activo',
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE Residente (
    id_residente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    ci VARCHAR(25) NULL UNIQUE,
    fecha_nac DATE NOT NULL,
    sexo ENUM('femenino', 'masculino', 'otro', 'no_especificado')
        NOT NULL DEFAULT 'no_especificado',
    direccion VARCHAR(200) NULL,
    telefono VARCHAR(8) NULL,
    contacto_emergencia VARCHAR(150) NULL,
    telefono_emergencia VARCHAR(8) NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_egreso DATE NULL,
    estado ENUM('activo', 'inactivo', 'egresado', 'fallecido') NOT NULL DEFAULT 'activo',
    observaciones TEXT NULL,
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_residente_ingreso CHECK (fecha_ingreso >= fecha_nac),
    CONSTRAINT chk_residente_egreso  CHECK (fecha_egreso IS NULL OR fecha_egreso >= fecha_ingreso),
    INDEX idx_residente_nombre (apellido, nombre)
) ENGINE=InnoDB;

CREATE TABLE Historial (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_residente INT NOT NULL,
    id_usuario INT NOT NULL,
    tipo_registro ENUM('patologia', 'alergia', 'antecedente', 'diagnostico', 'evolucion', 'otro')
        NOT NULL DEFAULT 'patologia',
    patologia VARCHAR(150) NULL,
    detalle TEXT NOT NULL,
    fecha DATE NOT NULL,
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_historial_residente FOREIGN KEY (id_residente)
        REFERENCES Residente(id_residente) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_historial_usuario FOREIGN KEY (id_usuario)
        REFERENCES Usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_historial_residente (id_residente, fecha)
) ENGINE=InnoDB;

CREATE TABLE Cuidado (
    id_cuidado INT AUTO_INCREMENT PRIMARY KEY,
    id_residente INT NOT NULL,
    id_usuario INT NOT NULL,
    tipo_cuidado VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    observaciones TEXT NULL,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cuidado_residente FOREIGN KEY (id_residente)
        REFERENCES Residente(id_residente) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_cuidado_usuario FOREIGN KEY (id_usuario)
        REFERENCES Usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_cuidado_residente (id_residente, fecha_hora)
) ENGINE=InnoDB;

CREATE TABLE Categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    descripcion VARCHAR(200) NULL
) ENGINE=InnoDB;

CREATE TABLE Proveedor (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL UNIQUE,
    telefono VARCHAR(8) NULL,
    correo VARCHAR(150) NULL,
    direccion VARCHAR(200) NULL,
    estado ENUM('activo', 'inactivo') NOT NULL DEFAULT 'activo'
) ENGINE=InnoDB;

CREATE TABLE Insumo (
    id_insumo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT NULL,
    id_categoria INT NOT NULL,
    unidad_medida VARCHAR(30) NOT NULL DEFAULT 'unidad',
    stock_min INT NOT NULL DEFAULT 0,
    estado ENUM('activo', 'inactivo') NOT NULL DEFAULT 'activo',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_insumo_stock_min CHECK (stock_min >= 0),
    CONSTRAINT fk_insumo_categoria FOREIGN KEY (id_categoria)
        REFERENCES Categoria(id_categoria) ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_insumo_nombre (nombre)
) ENGINE=InnoDB;

CREATE TABLE Medicamento (
    id_medicamento INT AUTO_INCREMENT PRIMARY KEY,
    id_insumo INT NOT NULL UNIQUE,
    principio_activo VARCHAR(120) NOT NULL,
    concentracion VARCHAR(60) NULL,
    forma VARCHAR(60) NULL,
    via_administracion VARCHAR(60) NULL,
    CONSTRAINT fk_medicamento_insumo FOREIGN KEY (id_insumo)
        REFERENCES Insumo(id_insumo) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE Lote (
    id_lote INT AUTO_INCREMENT PRIMARY KEY,
    codigo_lote VARCHAR(80) NOT NULL,
    id_insumo INT NOT NULL,
    id_proveedor INT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_vencimiento DATE NULL,
    stock_actual INT NOT NULL DEFAULT 0,
    observaciones VARCHAR(250) NULL,
    CONSTRAINT uq_lote_insumo_codigo UNIQUE (id_insumo, codigo_lote),
    CONSTRAINT chk_lote_stock  CHECK (stock_actual >= 0),
    CONSTRAINT chk_lote_fechas CHECK (fecha_vencimiento IS NULL OR fecha_vencimiento >= fecha_ingreso),
    CONSTRAINT fk_lote_insumo FOREIGN KEY (id_insumo)
        REFERENCES Insumo(id_insumo) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_lote_proveedor FOREIGN KEY (id_proveedor)
        REFERENCES Proveedor(id_proveedor) ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_lote_vencimiento (fecha_vencimiento)
) ENGINE=InnoDB;

CREATE TABLE Prescripcion (
    id_prescripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_residente INT NOT NULL,
    id_medicamento INT NOT NULL,
    id_usuario INT NOT NULL,
    dosis VARCHAR(80) NOT NULL,
    frecuencia VARCHAR(120) NOT NULL,
    indicaciones TEXT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NULL,
    estado ENUM('activa', 'finalizada', 'suspendida') NOT NULL DEFAULT 'activa',
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_prescripcion_fechas CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio),
    CONSTRAINT fk_prescripcion_residente FOREIGN KEY (id_residente)
        REFERENCES Residente(id_residente) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_prescripcion_medicamento FOREIGN KEY (id_medicamento)
        REFERENCES Medicamento(id_medicamento) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_prescripcion_usuario FOREIGN KEY (id_usuario)
        REFERENCES Usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_prescripcion_estado (estado, id_residente)
) ENGINE=InnoDB;

CREATE TABLE Movimiento (
    id_movimiento BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_lote INT NOT NULL,
    id_residente INT NULL,                 -- solo para salidas entregadas a un residente
    id_prescripcion INT NULL,
    id_usuario INT NOT NULL,
    tipo ENUM('entrada', 'salida') NOT NULL,
    cantidad INT NOT NULL,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observacion VARCHAR(250) NULL,
    CONSTRAINT chk_movimiento_cantidad CHECK (cantidad > 0),
    CONSTRAINT fk_movimiento_lote FOREIGN KEY (id_lote)
        REFERENCES Lote(id_lote) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_movimiento_residente FOREIGN KEY (id_residente)
        REFERENCES Residente(id_residente) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_movimiento_prescripcion FOREIGN KEY (id_prescripcion)
        REFERENCES Prescripcion(id_prescripcion) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_movimiento_usuario FOREIGN KEY (id_usuario)
        REFERENCES Usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_movimiento_fecha (fecha_hora)
) ENGINE=InnoDB;

DELIMITER $$

CREATE TRIGGER trg_movimiento_validar
BEFORE INSERT ON Movimiento
FOR EACH ROW
BEGIN
    DECLARE v_stock INT DEFAULT NULL;
    DECLARE v_venc DATE DEFAULT NULL;

    SELECT stock_actual, fecha_vencimiento
      INTO v_stock, v_venc
      FROM Lote
     WHERE id_lote = NEW.id_lote
     FOR UPDATE;

    IF v_stock IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El lote indicado no existe';
    END IF;

    IF NEW.tipo = 'salida' THEN
        IF v_venc IS NOT NULL AND v_venc < CURRENT_DATE THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede dar salida a un lote vencido';
        END IF;
        IF v_stock < NEW.cantidad THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock insuficiente en el lote';
        END IF;
    END IF;
END $$

CREATE TRIGGER trg_movimiento_actualizar_stock
AFTER INSERT ON Movimiento
FOR EACH ROW
BEGIN
    IF NEW.tipo = 'entrada' THEN
        UPDATE Lote SET stock_actual = stock_actual + NEW.cantidad
         WHERE id_lote = NEW.id_lote;
    ELSE
        UPDATE Lote SET stock_actual = stock_actual - NEW.cantidad
         WHERE id_lote = NEW.id_lote;
    END IF;
END $$

CREATE TRIGGER trg_movimiento_no_actualizar
BEFORE UPDATE ON Movimiento
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se permite modificar movimientos; registre uno nuevo';
END $$

CREATE TRIGGER trg_movimiento_no_eliminar
BEFORE DELETE ON Movimiento
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se permite eliminar movimientos';
END $$

DELIMITER ;

CREATE VIEW vw_stock_insumos AS
SELECT
    i.id_insumo,
    i.nombre AS insumo,
    c.nombre AS categoria,
    i.stock_min,
    COALESCE(SUM(CASE WHEN l.fecha_vencimiento IS NULL
                        OR l.fecha_vencimiento >= CURRENT_DATE
                      THEN l.stock_actual ELSE 0 END), 0) AS stock_disponible
FROM Insumo i
INNER JOIN Categoria c ON c.id_categoria = i.id_categoria
LEFT JOIN Lote l ON l.id_insumo = i.id_insumo
GROUP BY i.id_insumo, i.nombre, c.nombre, i.stock_min;

-- Lotes que vencen en los proximos 30 dias
CREATE VIEW vw_lotes_por_vencer AS
SELECT
    l.id_lote,
    l.codigo_lote,
    i.nombre AS insumo,
    l.stock_actual,
    l.fecha_vencimiento,
    DATEDIFF(l.fecha_vencimiento, CURRENT_DATE) AS dias_para_vencer
FROM Lote l
INNER JOIN Insumo i ON i.id_insumo = l.id_insumo
WHERE l.fecha_vencimiento BETWEEN CURRENT_DATE AND DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY)
  AND l.stock_actual > 0;

-- Lotes vencidos que todavia tienen stock
CREATE VIEW vw_lotes_vencidos AS
SELECT
    l.id_lote,
    l.codigo_lote,
    i.nombre AS insumo,
    l.stock_actual,
    l.fecha_vencimiento
FROM Lote l
INNER JOIN Insumo i ON i.id_insumo = l.id_insumo
WHERE l.fecha_vencimiento < CURRENT_DATE
  AND l.stock_actual > 0;
  
INSERT INTO Usuario (nombre, apellido, correo, contrasena, rol) VALUES
('Maria',  'Quispe', 'maria@hogar.com',  'hash_demo_1', 'administrador'),
('Carlos', 'Mamani', 'carlos@hogar.com', 'hash_demo_2', 'enfermeria'),
('Lucia',  'Flores', 'lucia@hogar.com',  'hash_demo_3', 'almacen'),
('Ana',    'Rojas',  'ana@hogar.com',    'hash_demo_4', 'cuidador');

INSERT INTO Residente (nombre, apellido, ci, fecha_nac, sexo, contacto_emergencia, telefono_emergencia, fecha_ingreso) VALUES
('Juan',  'Perez',   '1234567', '1940-05-10', 'masculino', 'Luis Perez',    '70011223', '2023-01-15'),
('Rosa',  'Choque',  '7654321', '1938-11-02', 'femenino',  'Elena Choque',  '70044556', '2022-08-20'),
('Pedro', 'Condori', '1112223', '1945-03-25', 'masculino', 'Marta Condori', '70099887', '2024-02-01'),
('Elena', 'Vargas',  '4445556', '1942-07-18', 'femenino',  'Raul Vargas',   '70055667', '2025-05-12');

INSERT INTO Historial (id_residente, id_usuario, tipo_registro, patologia, detalle, fecha) VALUES
(1, 2, 'patologia',   'Hipertension arterial', 'Controlada con tratamiento diario', '2023-01-15'),
(2, 2, 'alergia',     NULL,                    'Alergica a la penicilina',           '2022-08-20'),
(3, 2, 'patologia',   'Diabetes tipo 2',       'Requiere control de glucemia',       '2024-02-01'),
(4, 2, 'antecedente', NULL,                    'Fractura de cadera en 2021',         '2025-05-12');

INSERT INTO Cuidado (id_residente, id_usuario, tipo_cuidado, descripcion) VALUES
(1, 2, 'Control de signos vitales', 'Presion 130/85, pulso 72'),
(2, 4, 'Higiene personal',          'Bano asistido en la manana'),
(3, 2, 'Control de glucemia',       'Glucemia en ayunas 118 mg/dl'),
(4, 4, 'Movilizacion',              'Caminata asistida de 15 minutos');

INSERT INTO Categoria (nombre, descripcion) VALUES
('Medicamentos',    'Medicamentos y productos farmacologicos'),
('Insumos medicos', 'Material de curacion y atencion medica'),
('Higiene',         'Productos de higiene y aseo personal');

INSERT INTO Proveedor (nombre, telefono, correo, direccion) VALUES
('Farmacia Central',    '2200011', 'ventas@farmaciacentral.com', 'Av. Camacho 123'),
('Distribuidora Salud', '2200022', 'info@distsalud.com',         'Calle Comercio 456');

INSERT INTO Insumo (nombre, id_categoria, unidad_medida, stock_min) VALUES
('Losartan 50mg',       1, 'tableta', 30),
('Metformina 850mg',    1, 'tableta', 30),
('Paracetamol 500mg',   1, 'tableta', 40),
('Guantes de latex',    2, 'caja',     5),
('Panales para adulto', 3, 'paquete', 10);

INSERT INTO Medicamento (id_insumo, principio_activo, concentracion, forma, via_administracion) VALUES
(1, 'Losartan',     '50 mg',  'tableta', 'oral'),
(2, 'Metformina',   '850 mg', 'tableta', 'oral'),
(3, 'Paracetamol',  '500 mg', 'tableta', 'oral');

INSERT INTO Lote (codigo_lote, id_insumo, id_proveedor, fecha_ingreso, fecha_vencimiento) VALUES
('L001', 1, 1, '2026-09-01', '2027-09-01'),
('L002', 2, 1, '2026-09-01', '2027-06-01'),
('L003', 3, 1, '2026-06-01', '2026-10-01'),   -- ya vencido
('L004', 4, 2, '2026-10-10', NULL),
('L005', 5, 2, '2026-10-10', NULL),
('L006', 3, 1, '2026-10-20', '2026-12-05');   -- vence pronto

INSERT INTO Prescripcion (id_residente, id_medicamento, id_usuario, dosis, frecuencia, fecha_inicio) VALUES
(1, 1, 2, '1 tableta', 'cada 24 horas', '2026-09-05'),
(3, 2, 2, '1 tableta', 'cada 12 horas', '2026-09-05'),
(2, 3, 2, '1 tableta', 'cada 8 horas',  '2026-10-25');

INSERT INTO Movimiento (id_lote, id_usuario, tipo, cantidad, observacion) VALUES
(1, 3, 'entrada', 100, 'Compra inicial'),
(2, 3, 'entrada',  80, 'Compra inicial'),
(3, 3, 'entrada',  20, 'Compra inicial'),
(4, 3, 'entrada',   4, 'Compra inicial'),
(5, 3, 'entrada',  30, 'Compra inicial'),
(6, 3, 'entrada',  50, 'Compra inicial');

INSERT INTO Movimiento (id_lote, id_residente, id_prescripcion, id_usuario, tipo, cantidad, observacion) VALUES
(1, 1, 1, 3, 'salida', 10, 'Entrega semanal'),
(2, 3, 2, 3, 'salida', 14, 'Entrega semanal'),
(6, 2, 3, 3, 'salida', 21, 'Entrega semanal');

INSERT INTO Movimiento (id_lote, id_usuario, tipo, cantidad, observacion) VALUES
(5, 3, 'salida', 8, 'Consumo del turno noche');

SELECT id_residente, nombre, apellido,
       TIMESTAMPDIFF(YEAR, fecha_nac, CURDATE()) AS edad,
       fecha_ingreso
FROM Residente
WHERE estado = 'activo'
ORDER BY apellido;

SELECT CONCAT(r.nombre, ' ', r.apellido) AS residente,
       h.tipo_registro, h.patologia, h.detalle, h.fecha
FROM Residente r
INNER JOIN Historial h ON h.id_residente = r.id_residente
ORDER BY r.apellido, h.fecha;

SELECT CONCAT(r.nombre, ' ', r.apellido) AS residente,
       i.nombre AS medicamento, p.dosis, p.frecuencia,
       CONCAT(u.nombre, ' ', u.apellido) AS registrado_por
FROM Prescripcion p
INNER JOIN Residente r   ON r.id_residente = p.id_residente
INNER JOIN Medicamento m ON m.id_medicamento = p.id_medicamento
INNER JOIN Insumo i      ON i.id_insumo = m.id_insumo
INNER JOIN Usuario u     ON u.id_usuario = p.id_usuario
WHERE p.estado = 'activa';

SELECT insumo, categoria, stock_min, stock_disponible,
       CASE
           WHEN stock_disponible = 0 THEN 'AGOTADO'
           WHEN stock_disponible <= stock_min THEN 'STOCK BAJO'
           ELSE 'DISPONIBLE'
       END AS estado_stock
FROM vw_stock_insumos
ORDER BY categoria, insumo;

SELECT * FROM vw_lotes_por_vencer;
SELECT * FROM vw_lotes_vencidos;

SELECT CONCAT(r.nombre, ' ', r.apellido) AS residente,
       i.nombre AS medicamento,
       SUM(mv.cantidad) AS unidades_entregadas
FROM Movimiento mv
INNER JOIN Residente r ON r.id_residente = mv.id_residente
INNER JOIN Lote l      ON l.id_lote = mv.id_lote
INNER JOIN Insumo i    ON i.id_insumo = l.id_insumo
WHERE mv.tipo = 'salida'
GROUP BY r.id_residente, r.nombre, r.apellido, i.id_insumo, i.nombre;

SELECT CONCAT(u.nombre, ' ', u.apellido) AS usuario,
       mv.tipo, COUNT(*) AS total_movimientos, SUM(mv.cantidad) AS total_unidades
FROM Movimiento mv
INNER JOIN Usuario u ON u.id_usuario = mv.id_usuario
GROUP BY u.id_usuario, u.nombre, u.apellido, mv.tipo;

SELECT CONCAT(r.nombre, ' ', r.apellido) AS residente, COUNT(*) AS cuidados
FROM Residente r
INNER JOIN Cuidado c ON c.id_residente = r.id_residente
GROUP BY r.id_residente, r.nombre, r.apellido
HAVING COUNT(*) > 1;

SELECT nombre, apellido
FROM Residente
WHERE id_residente NOT IN (SELECT id_residente FROM Prescripcion);

SELECT i.nombre
FROM Insumo i
WHERE i.id_insumo NOT IN (
    SELECT l.id_insumo
    FROM Movimiento mv
    INNER JOIN Lote l ON l.id_lote = mv.id_lote
    WHERE mv.tipo = 'salida'
);

USE gestion_tercera_edad;

SHOW TRIGGERS FROM gestion_tercera_edad;

SHOW CREATE TRIGGER trg_movimiento_validar;

SHOW CREATE TRIGGER trg_movimiento_actualizar_stock;

SHOW CREATE TRIGGER trg_movimiento_validar;

SELECT ACTION_STATEMENT
FROM information_schema.TRIGGERS
WHERE TRIGGER_SCHEMA = 'gestion_tercera_edad'
AND TRIGGER_NAME = 'trg_movimiento_validar';

USE gestion_tercera_edad;

UPDATE Usuario
SET correo = 'mateo@hogar.com'
WHERE correo = 'maria@hogar.com';

SELECT id_usuario, nombre, apellido, correo, rol
FROM Usuario
WHERE correo = 'mateo@hogar.com';

USE gestion_tercera_edad;

UPDATE Usuario
SET nombre = 'Mateo',
    correo = 'mateo@hogar.com'
WHERE correo IN ('maria@hogar.com', 'mateo@hogar.com');

SELECT id_usuario, nombre, apellido, correo, rol
FROM Usuario
WHERE correo = 'mateo@hogar.com';

USE gestion_tercera_edad;

UPDATE Usuario
SET nombre = 'Mateo',
    apellido = 'Camacho',
    correo = 'mateo@hogar.com'
WHERE correo IN ('maria@hogar.com', 'mateo@hogar.com');

SELECT id_usuario, nombre, apellido, correo, rol
FROM Usuario
WHERE correo = 'mateo@hogar.com';

CREATE USER IF NOT EXISTS 'gestion_app'@'localhost'
IDENTIFIED BY 'unifranz456';

GRANT SELECT, INSERT, UPDATE
ON gestion_tercera_edad.*
TO 'gestion_app'@'localhost';

SHOW GRANTS FOR 'gestion_app'@'localhost';

USE gestion_tercera_edad;

SHOW TRIGGERS
FROM gestion_tercera_edad;

SHOW GRANTS FOR 'gestion_app'@'localhost';

SHOW GRANTS FOR 'gestion_app'@'localhost';

USE gestion_tercera_edad;

SHOW CREATE TRIGGER trg_movimiento_validar;

SHOW CREATE TRIGGER trg_movimiento_actualizar_stock;

SHOW CREATE TRIGGER trg_movimiento_validar;

SHOW CREATE TABLE Movimiento;

SHOW CREATE TRIGGER trg_movimiento_no_actualizar;

SHOW CREATE TRIGGER trg_movimiento_no_eliminar;

SHOW CREATE TRIGGER trg_movimiento_no_actualizar;

USE gestion_tercera_edad;

SELECT
    l.codigo_lote,
    i.nombre AS insumo,
    l.stock_actual
FROM Lote l
INNER JOIN Insumo i ON l.id_insumo = i.id_insumo
WHERE l.codigo_lote = 'TEST-GASAS-001';

SELECT
    l.id_lote,
    l.codigo_lote,
    l.id_insumo,
    i.nombre AS nombre_insumo,
    l.stock_actual
FROM Lote l
JOIN Insumo i ON l.id_insumo = i.id_insumo
WHERE l.codigo_lote = 'TEST-GASAS-001';

SELECT codigo_lote, stock_actual
FROM Lote
WHERE codigo_lote = 'TEST-GASAS-001';

USE gestion_tercera_edad;

SELECT
    l.id_lote,
    l.codigo_lote,
    i.nombre AS insumo,
    l.fecha_vencimiento,
    l.stock_actual
FROM Lote l
INNER JOIN Insumo i ON l.id_insumo = i.id_insumo
WHERE l.fecha_vencimiento < CURDATE()
  AND l.stock_actual > 0
ORDER BY l.fecha_vencimiento;

SHOW GRANTS FOR 'gestion_app'@'localhost';
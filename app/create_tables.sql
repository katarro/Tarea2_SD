CREATE TABLE regular_topic (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    phone VARCHAR(50),
    type VARCHAR(50),
    password VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE paid_topic (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    phone VARCHAR(50),
    type VARCHAR(50) CHECK (type IN ('normal', 'paid')),
    password VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE Maestros (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    phone VARCHAR(50),
    type VARCHAR(50) CHECK (type IN ('normal', 'paid')),
    password VARCHAR(255),
    email VARCHAR(255),
    aprobado BOOLEAN DEFAULT FALSE
);

CREATE TABLE Ingredientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE StockIngredientes (
    id_maestro INTEGER REFERENCES Maestros(id),
    id_ingrediente INTEGER REFERENCES Ingredientes(id),
    stock INTEGER CHECK (stock >= 0),
    PRIMARY KEY (id_maestro, id_ingrediente)
);

CREATE TABLE Inscripciones (
    id SERIAL PRIMARY KEY,
    id_maestro INTEGER REFERENCES Maestros(id),
    fecha DATE NOT NULL,
    estado VARCHAR(50) CHECK (estado IN ('pendiente', 'aprobada', 'rechazada'))
);

CREATE TABLE NotificacionesStock (
    id SERIAL PRIMARY KEY,
    id_maestro INTEGER,
    id_ingrediente INTEGER,
    fecha DATE NOT NULL,
    cantidad INTEGER CHECK (cantidad > 0),
    FOREIGN KEY (id_maestro, id_ingrediente) REFERENCES StockIngredientes(id_maestro, id_ingrediente)
);

CREATE TABLE Ventas (
    id SERIAL PRIMARY KEY,
    id_maestro INTEGER REFERENCES Maestros(id),
    fecha DATE NOT NULL,
    monto DECIMAL CHECK (monto >= 0)
);


CREATE TABLE Postres (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL,
    precio DECIMAL CHECK (precio > 0)
);

CREATE TABLE IngredientesPostre (
    id_postre INTEGER REFERENCES Postres(id),
    id_ingrediente INTEGER REFERENCES Ingredientes(id),
    cantidad INTEGER CHECK (cantidad > 0),
    PRIMARY KEY (id_postre, id_ingrediente)
);

-- Insertar los ingredientes
INSERT INTO Ingredientes (nombre) VALUES ('mote'), ('huesillo');

-- Insertar el postre
INSERT INTO Postres (nombre, precio) VALUES ('mote con huesillo', 1500);

-- Obtener los IDs de los ingredientes y el postre
-- Supongamos que los IDs son 1 para 'mote', 2 para 'huesillo' y 1 para 'mote con huesillo'

-- Relacionar los ingredientes con el postre
INSERT INTO IngredientesPostre (id_postre, id_ingrediente, cantidad) VALUES (1, 1, 1), (1, 2, 1);


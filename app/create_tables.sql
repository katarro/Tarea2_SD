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
    type VARCHAR(50),
    password VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE maestros (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    tipo VARCHAR(50) CHECK (tipo IN ('normal', 'paid')),
);

CREATE TABLE ingredientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE stock_ingredientes (
    id_maestro INTEGER REFERENCES Maestros(id),
    id_ingrediente INTEGER REFERENCES Ingredientes(id),
    stock INTEGER CHECK (stock >= 0),
    PRIMARY KEY (id_maestro, id_ingrediente)
);

CREATE TABLE inscripciones (
    id SERIAL PRIMARY KEY,
    id_maestro INTEGER REFERENCES Maestros(id),
    fecha DATE NOT NULL,
    estado VARCHAR(50) CHECK (estado IN ('pendiente', 'aprobada', 'rechazada'))
);

CREATE TABLE notificaciones_stock (
    id SERIAL PRIMARY KEY,
    id_stock_ingredientes INTEGER,
    fecha DATE NOT NULL,
    cantidad INTEGER CHECK (cantidad > 0),
    FOREIGN KEY (id_stock_ingredientes) REFERENCES StockIngredientes(id_maestro, id_ingrediente)
);

CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    id_maestro INTEGER REFERENCES Maestros(id),
    fecha DATE NOT NULL,
    monto DECIMAL CHECK (monto >= 0)
);

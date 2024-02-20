# TABLAS MOMO ECONOMIA

## 1. Tabla de Usuarios (users)
    - user_id: Identificador único del usuario en Discord.
    - guild_id: Identificador único del servidor (guild) de Discord.
    - sername: Nombre de usuario en Discord.
    - balance: Balance actual de monedas del usuario.
    
```sql
-- Tabla de Usuarios (users)
CREATE TABLE users (
    userid BIGINT,
    guildid BIGINT,
    username VARCHAR(255),
    balance INT DEFAULT 0,
    PRIMARY KEY (userid, guildid)
);
```

## 2. Tabla de Transacciones (transactions)
    - transaction_id: Identificador único de la transacción.
    - user_id: Identificador del usuario que realiza la transacción, relacionado con users.user_id.
    - guild_id: Identificador del servidor, relacionado con users.guild_id.
    - amount: Monto de la transacción. Puede ser positivo (ganancia) o negativo (gasto).
    - type: Tipo de transacción (p.ej., trabajo, compra, recompensa).
    - timestamp: Fecha y hora de la transacción.


3. Tabla de Trabajos (jobs)
    job_id: Identificador único del trabajo.
    guild_id: Identificador del servidor donde está disponible el trabajo.
    job_name: Nombre del trabajo.
    payout: Rango de pago por realizar el trabajo.
4. Tabla de Recompensas (rewards)
    reward_id: Identificador único de la recompensa.
    guild_id: Identificador del servidor donde está disponible la recompensa.
    description: Descripción de la recompensa.
    cost: Costo en monedas para reclamar la recompensa.
5. Tabla de Artículos de la Tienda (shop_items)
    item_id: Identificador único del artículo.
    guild_id: Identificador del servidor donde está disponible el artículo.
    item_name: Nombre del artículo.
    price: Precio del artículo.
6. Tabla de Registros de Compras (purchase_logs)
    purchase_id: Identificador único de la compra.
    user_id: Identificador del usuario que realiza la compra, relacionado con users.user_id.
    item_id: Identificador del artículo comprado, relacionado con shop_items.item_id.
    guild_id: Identificador del servidor, relacionado con users.guild_id.
    timestamp: Fecha y hora de la compra.

Relaciones entre las tablas:
    Usuarios y Transacciones: Cada transacción está vinculada a un usuario y un servidor específicos. Esto permite rastrear todas las transacciones (trabajos realizados, compras, etc.) de cada usuario en cada servidor.
    Usuarios y Registros de Compras: Cada registro de compra está vinculado a un usuario específico y a un artículo de la tienda, lo que permite rastrear qué usuario ha comprado qué artículo.
    Artículos de la Tienda y Registros de Compras: Cada registro de compra se relaciona con un artículo específico de la tienda, lo que permite rastrear las ventas de cada artículo.





-- Tabla de Transacciones (transactions)
CREATE TABLE transactions (
    transactionid INT AUTOINCREMENT PRIMARY KEY,
    userid BIGINT,
    guildid BIGINT,
    amount INT,
    type VARCHAR(50),
    timestamp DATETIME,
    FOREIGN KEY (userid, guildid) REFERENCES users(userid, guildid)
);

--  Tabla de Trabajos (jobs)
CREATE TABLE jobs (
    jobid INT AUTOINCREMENT PRIMARY KEY,
    guildid BIGINT,
    jobname VARCHAR(255),
    payout INT
);

-- Tabla de Recompensas (rewards)
CREATE TABLE rewards (
    rewardid INT AUTOINCREMENT PRIMARY KEY,
    guildid BIGINT,
    description TEXT,
    cost INT
);

-- Tabla de Artículos de la Tienda (shopitems)
CREATE TABLE shopitems (
    itemid INT AUTOINCREMENT PRIMARY KEY,
    guildid BIGINT,
    itemname VARCHAR(255),
    price INT
);

-- Tabla de Registros de Compras (purchaselogs)
CREATE TABLE purchaselogs (
    purchaseid INT AUTOINCREMENT PRIMARY KEY,
    userid BIGINT,
    itemid INT,
    guildid BIGINT,
    timestamp DATETIME,
    FOREIGN KEY (userid, guildid) REFERENCES users(userid, guildid),
    FOREIGN KEY (itemid) REFERENCES shopitems(itemid)
);

-- Tabla de Logros
CREATE TABLE achievements (
    achievementid INT AUTOINCREMENT PRIMARY KEY,
    guildid BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    reward INT NOT NULL
);

-- Tabla de Progreso de Logros del Usuario
CREATE TABLE userachievements (
    userid BIGINT NOT NULL,
    achievementid INT NOT NULL,
    guildid BIGINT NOT NULL,
    achievedon DATETIME NOT NULL,
    PRIMARY KEY (userid, achievementid, guildid),
    FOREIGN KEY (achievementid) REFERENCES achievements(achievementid)
);

-- Tabla de Inventario del Usuario
CREATE TABLE userinventory (
    inventoryid INT AUTOINCREMENT PRIMARY KEY,
    userid BIGINT NOT NULL,
    itemid INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (itemid) REFERENCES shopitems(itemid)
);

-- Tabla de Misiones
CREATE TABLE quests (
    questid INT AUTOINCREMENT PRIMARY KEY,
    guildid BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    reward INT NOT NULL
);

-- Tabla de Progreso de Misiones del Usuario
CREATE TABLE userquests (
    userid BIGINT NOT NULL,
    questid INT NOT NULL,
    guildid BIGINT NOT NULL,
    status VARCHAR(50) NOT NULL,
    progress INT DEFAULT 0,
    PRIMARY KEY (userid, questid, guildid),
    FOREIGN KEY (questid) REFERENCES quests(questid)
);

-- Tabla de Eventos Especiales
CREATE TABLE specialevents (
    eventid INT AUTOINCREMENT PRIMARY KEY,
    guildid BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    starttime DATETIME NOT NULL,
    endtime DATETIME NOT NULL
);


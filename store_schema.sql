PRAGMA foreign_keys=off;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  username    varchar(50) not null unique,
  password    varchar(50) not null,
  PRIMARY KEY (username)
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  order_id      int(4) not null unique,
  date_time     varchar(50) not null,
  ordered_by    varchar(50) not null,
  total         int(4) not null,
  FOREIGN KEY (ordered_by) REFERENCES users(username)
);

DROP TABLE IF EXISTS order_item;
CREATE TABLE order_item (
  order_id        int(4) not null unique,
  date_time       varchar(50) not null,
  ordered_by      varchar(50) not null,
  quantity        int(4) not null,
  FOREIGN KEY (ordered_by) REFERENCES users(username),
  FOREIGN KEY (date_time) REFERENCES orders(date_time)
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
  product_id        int(4) not null unique,
  name              varchar(50) not null,
  stock             int(4) not null,
  price             decimal(4, 2) not null,
  description       varchar(100) not null,
  part_of           varchar(50) not null,
  PRIMARY KEY (product_id),
  FOREIGN KEY (part_of) REFERENCES categories(category)
);

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
  category  varchar(50),
  PRIMARY KEY (category)
);

PRAGMA foreign_keys=on;

INSERT INTO users VALUES ('testuser', 'testpass');

INSERT INTO categories VALUES ('Socks');
INSERT INTO products VALUES ('0001', 'pinksocks', '5', '5.99', 'These socks are pink!', 'Socks');
INSERT INTO products VALUES ('0002', 'bluesocks', '5', '5.99', 'These socks are blue!', 'Socks');
INSERT INTO products VALUES ('0003', 'blacksocks', '10', '4.99', 'These socks are black!', 'Socks');
INSERT INTO products VALUES ('0004', 'whitesocks', '10', '4.99', 'These socks are white!', 'Socks');

INSERT INTO categories VALUES ('Underwear');
INSERT INTO products VALUES ('0005', 'purplewear', '5', '8.99', 'This underwear is purple!', 'Underwear');
INSERT INTO products VALUES ('0006', 'redwear', '5', '8.99', 'This underwear is red!', 'Underwear');
INSERT INTO products VALUES ('0007', 'greenwear', '5', '9.99', 'This underwear is green!', 'Underwear');

INSERT INTO categories VALUES ('Hats');
INSERT INTO products VALUES ('0008', 'brownhat', '5', '6.99', 'This hat is brown!', 'Hats');
INSERT INTO products VALUES ('0009', 'orangehat', '5', '6.99', 'This hat is orange!', 'Hats');
INSERT INTO products VALUES ('00010', 'yellowhat', '10', '7.99', 'This hat is yellow!', 'Hats');

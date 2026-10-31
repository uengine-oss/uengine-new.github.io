-- Hanbit Delivery legacy order system DB (tutorial exercise) — schema delivery
CREATE SCHEMA IF NOT EXISTS delivery;
SET search_path = delivery;

CREATE TABLE store (
  store_id    varchar(10) PRIMARY KEY,
  store_name  varchar(60) NOT NULL,
  owner_name  varchar(30) NOT NULL,
  district    varchar(30) NOT NULL,
  is_open     boolean     NOT NULL DEFAULT true
);
CREATE TABLE menu (
  menu_id     varchar(10) PRIMARY KEY,
  store_id    varchar(10) NOT NULL REFERENCES store(store_id),
  menu_name   varchar(60) NOT NULL,
  price       integer     NOT NULL CHECK (price > 0),
  sold_out    boolean     NOT NULL DEFAULT false
);
CREATE TABLE customer (
  customer_id varchar(10) PRIMARY KEY,
  customer_name varchar(30) NOT NULL,
  phone       varchar(20) NOT NULL,
  address     varchar(100) NOT NULL
);
CREATE TABLE orders (
  order_id    varchar(12) PRIMARY KEY,
  customer_id varchar(10) NOT NULL REFERENCES customer(customer_id),
  store_id    varchar(10) NOT NULL REFERENCES store(store_id),
  status      varchar(20) NOT NULL,  -- WAITING, ACCEPTED, COOKING, DELIVERING, DELIVERED, CANCELLED, REJECTED
  total_price integer     NOT NULL,
  ordered_at  timestamp   NOT NULL
);
CREATE TABLE order_item (
  order_id    varchar(12) NOT NULL REFERENCES orders(order_id),
  menu_id     varchar(10) NOT NULL REFERENCES menu(menu_id),
  qty         integer     NOT NULL CHECK (qty > 0),
  unit_price  integer     NOT NULL,
  PRIMARY KEY (order_id, menu_id)
);
CREATE TABLE rider (
  rider_id    varchar(10) PRIMARY KEY,
  rider_name  varchar(30) NOT NULL,
  vehicle     varchar(20) NOT NULL
);
CREATE TABLE delivery (
  delivery_id varchar(12) PRIMARY KEY,
  order_id    varchar(12) NOT NULL REFERENCES orders(order_id),
  rider_id    varchar(10) REFERENCES rider(rider_id),
  picked_up_at timestamp,
  delivered_at timestamp
);

INSERT INTO store VALUES
 ('S001','Hanbit Snacks','Kim','Mapo-gu',true),
 ('S002','Bada Sashimi','Lee','Seodaemun-gu',true),
 ('S003','Alley Chicken','Park','Mapo-gu',false);
INSERT INTO menu VALUES
 ('M001','S001','Tteokbokki',5000,false),('M002','S001','Gimbap',3500,false),('M003','S001','Sundae',4500,true),
 ('M004','S002','Assorted sashimi',38000,false),('M005','S002','Spicy fish stew',15000,false),
 ('M006','S003','Fried chicken',19000,false),('M007','S003','Seasoned chicken',21000,false);
INSERT INTO customer VALUES
 ('C001','Haneul Jung','010-1111-2222','12 Yeonnam-dong, Mapo-gu'),
 ('C002','Bada Choi','010-3333-4444','7 Sinchon-dong, Seodaemun-gu'),
 ('C003','Garam Yoon','010-5555-6666','33 Mangwon-dong, Mapo-gu');
INSERT INTO orders VALUES
 ('O2026103001','C001','S001','DELIVERED',13500,'2026-10-30 11:20'),
 ('O2026103002','C002','S002','DELIVERING',38000,'2026-10-30 12:05'),
 ('O2026103003','C003','S001','CANCELLED',5000,'2026-10-30 12:40'),
 ('O2026103004','C001','S003','REJECTED',19000,'2026-10-30 13:10'),
 ('O2026103005','C003','S002','COOKING',53000,'2026-10-30 18:30');
INSERT INTO order_item VALUES
 ('O2026103001','M001',2,5000),('O2026103001','M002',1,3500),
 ('O2026103002','M004',1,38000),
 ('O2026103003','M001',1,5000),
 ('O2026103004','M006',1,19000),
 ('O2026103005','M004',1,38000),('O2026103005','M005',1,15000);
INSERT INTO rider VALUES ('R001','Rider Han','motorcycle'),('R002','Rider Kang','bicycle');
INSERT INTO delivery VALUES
 ('D001','O2026103001','R001','2026-10-30 11:40','2026-10-30 12:02'),
 ('D002','O2026103002','R002','2026-10-30 12:35',NULL);

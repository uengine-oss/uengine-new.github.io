-- 한빛 딜리버리 기존 주문 시스템 DB (튜토리얼 실습용) — 스키마 delivery
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
 ('S001','한빛분식','김사장','마포구',true),
 ('S002','바다횟집','이사장','서대문구',true),
 ('S003','골목치킨','박사장','마포구',false);
INSERT INTO menu VALUES
 ('M001','S001','떡볶이',5000,false),('M002','S001','김밥',3500,false),('M003','S001','순대',4500,true),
 ('M004','S002','모둠회',38000,false),('M005','S002','매운탕',15000,false),
 ('M006','S003','후라이드',19000,false),('M007','S003','양념치킨',21000,false);
INSERT INTO customer VALUES
 ('C001','정하늘','010-1111-2222','마포구 연남동 12'),
 ('C002','최바다','010-3333-4444','서대문구 신촌동 7'),
 ('C003','윤가람','010-5555-6666','마포구 망원동 33');
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
INSERT INTO rider VALUES ('R001','한라이더','오토바이'),('R002','강라이더','자전거');
INSERT INTO delivery VALUES
 ('D001','O2026103001','R001','2026-10-30 11:40','2026-10-30 12:02'),
 ('D002','O2026103002','R002','2026-10-30 12:35',NULL);

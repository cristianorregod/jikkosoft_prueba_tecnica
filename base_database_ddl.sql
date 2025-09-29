-- Migrations for the base database schema

create table users (
  id uuid primary key,
  email text unique,
  password_hash text,
  role text,
  created_at timestamp
);

create table restaurants (
  id uuid primary key,
  name text,
  address text,
  latitude numeric(9, 6),
  longitude numeric(9, 6),
  status text,
  created_at timestamp
);

create table menu_items (
  id uuid primary key,
  restaurant_id uuid references restaurants (id),
  name text,
  price numeric(12, 2),
  active boolean
);

create table orders (
  id uuid primary key,
  customer_id uuid references users (id),
  restaurant_id uuid references restaurants (id),
  status text,
  subtotal numeric(12, 2),
  shipping numeric(12, 2),
  discount numeric(12, 2),
  total numeric(12, 2),
  created_at timestamp,
  updated_at timestamp
);

create table order_items (
  id uuid primary key,
  order_id uuid references orders (id),
  menu_item_id uuid references menu_items (id),
  quantity int,
  price numeric(12, 2)
);

create table drivers (
  id uuid primary key,
  user_id uuid references users (id),
  status text,
  vehicle_info jsonb
);

create table payments (
  id uuid primary key,
  order_id uuid references orders (id),
  amount numeric(12, 2) not null,
  currency char(3) default 'COP',
  method text not null,
  status text not null,
  provider_transaction_id text,
  provider_response jsonb,
  created_at timestamp default now(),
  updated_at timestamp default now(),
  refunded_amount numeric(12, 2) default 0,
  retry_count int default 0
);
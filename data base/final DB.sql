create table customers (
cust_id int  primary key,
phone varchar(20) not null ,
name nvarchar(100) not null ,
address nvarchar(100) , 
email nvarchar(100) ,
password nvarchar(100) ,
);

create table categories (
category_id int  primary key,
name nvarchar(100) not null,
unique (name));

create table products(
prod_id int  primary key ,
name nvarchar(100) not null ,
description nvarchar(100)  ,
category_id int foreign key references categories (category_id)
);

--we need a trigger to track the total price and avoid reduncacy 
create table orders (
order_id int  primary key ,
date date ,
status nvarchar(100) ,
cust_id int foreign key references customers (cust_id)
on delete cascade
);

create table cust_cart (
cart_id int primary key ,
cust_id int foreign key references customers (cust_id) 
on delete cascade,-- if the customer do not have a cart the cart will not exist 
unique (cust_id)--the relation is one to one 
) 

--we can derive the quantity using an aggregate function SUM(quantity) from order items so we don't want 
--we donot want the quantity feild here 
create table cart_include_products(
cart_prod_id int  primary key ,
product_id int ,
cart_id int ,
quantity int not null ,
foreign key (cart_id) references cust_cart (cart_id)
on delete cascade,
foreign key (product_id) references products (prod_id)
on delete cascade,
unique(cart_id , product_id)
);

create table shipment (
shipment_id int  primary key ,
method nvarchar (100),
date date ,
status nvarchar (100),
address nvarchar(100),
order_id int foreign key references orders(order_id)
on delete cascade,
unique (order_id)
);
create table payment (
transaction_id int  primary key ,
method nvarchar(100) ,--cash , credit , paypal and so on 
amount int ,
date date,
order_id int foreign key references orders(order_id) 
on delete cascade,
unique (order_id)
);

create table order_items (
order_item_id int  primary key ,
order_id int ,
product_id int ,
foreign key (order_id) references orders(order_id)
on delete cascade ,
foreign key (product_id) references products(prod_id)
on delete cascade ,
quantity int not null ,
price decimal (10,2) not null ,
unique (order_id , product_id)
);
-- Insert into categories
INSERT INTO categories (category_id, name) VALUES 
(211, 'Electronics'), 
(212, 'Books'), 
(213, 'Clothing'), 
(214, 'Toys'), 
(215, 'Furniture'), 
(216, 'Home Appliances'), 
(217, 'Groceries'), 
(218, 'Beauty & Personal Care'), 
(219, 'Sports & Outdoors'), 
(220, 'Automotive');

-- Insert into customers
INSERT INTO customers (cust_id, phone, name, address, email, password) VALUES
(301, '1234567890', 'Ali Hassan', 'Cairo, Egypt', 'ali@example.com', 'pass1234'),
(302, '9876543210', 'Mona Ahmed', 'Alexandria, Egypt', 'mona@example.com', 'pass5678'),
(303, '5556667777', 'Ahmed Youssef', 'Giza, Egypt', 'ahmed@example.com', 'pass9101'),
(304, '9998887776', 'Om Ali', 'Tanta, Egypt', 'om.ali@example.com', 'pass1121'),
(305, '6665554443', 'Omar Khaled', 'Ismailia, Egypt', 'omar@example.com', 'pass3141'),
(306, '1112223334', 'Laila Mostafa', 'Fayoum, Egypt', 'laila@example.com', 'pass5161'),
(307, '4445556667', 'Hassan Mahmoud', 'Suez, Egypt', 'hassan@example.com', 'pass7181'),
(308, '7778889990', 'Noha Sameh', 'Aswan, Egypt', 'noha@example.com', 'pass9201'),
(309, '3332221110', 'Ramy Nabil', 'Luxor, Egypt', 'ramy@example.com', 'pass1222'),
(310, '8887776665', 'Nour Adel', 'Mansoura, Egypt', 'nour@example.com', 'pass3243');

-- Insert into products
INSERT INTO products (prod_id, name, description, category_id) VALUES
(401, 'Smartphone', 'Latest model', 211),
(402, 'Laptop', 'High performance', 211),
(403, 'Headphones', 'Noise cancelling', 211),
(404, 'Camera', 'DSLR with lenses', 211),
(405, 'Book', 'Fiction novel', 212),
(406, 'T-shirt', 'Cotton, size M', 213),
(407, 'Toy', 'Lego set', 214),
(408, 'Sofa', 'Leather', 215),
(409, 'Blender', 'High power', 216),
(410, 'Basketball', 'Outdoor use', 219);

-- Insert into orders
INSERT INTO orders (order_id, date, status, cust_id) VALUES
(501, '2024-01-01', 'Pending', 301),
(502, '2024-01-02', 'Shipped', 302),
(503, '2024-01-03', 'Delivered', 303),
(504, '2024-01-04', 'Cancelled', 304),
(505, '2024-01-05', 'Returned', 305),
(506, '2024-01-06', 'Pending', 306),
(507, '2024-01-07', 'Shipped', 307),
(508, '2024-01-08', 'Delivered', 308),
(509, '2024-01-09', 'Cancelled', 309),
(510, '2024-01-10', 'Returned', 310);

-- Insert into cust_cart
INSERT INTO cust_cart (cart_id, cust_id) VALUES
(601, 301),
(602, 302),
(603, 303),
(604, 304),
(605, 305),
(606, 306),
(607, 307),
(608, 308),
(609, 309),
(610, 310);

-- Insert into cart_include_products
INSERT INTO cart_include_products (cart_prod_id, product_id, cart_id, quantity) VALUES
(701, 401, 601, 2),
(702, 402, 602, 1),
(703, 403, 603, 3),
(704, 404, 604, 1),
(705, 405, 605, 5),
(706, 406, 606, 2),
(707, 407, 607, 3),
(708, 408, 608, 4),
(709, 409, 609, 1),
(710, 410, 610, 2);

-- Insert into order_items
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, price) VALUES
(801, 501, 401, 2, 299.99),
(802, 502, 402, 1, 499.99),
(803, 503, 403, 3, 199.99),
(804, 504, 404, 1, 99.99),
(805, 505, 405, 5, 39.99),
(806, 506, 406, 2, 24.99),
(807, 507, 407, 3, 79.99),
(808, 508, 408, 4, 49.99),
(809, 509, 409, 1, 19.99),
(810, 510, 410, 2, 9.99);

-- Insert into payment
INSERT INTO payment (transaction_id, method, amount, date, order_id) VALUES
(901, 'Credit Card', 599.98, '2024-01-01', 501),
(902, 'PayPal', 599.97, '2024-01-02', 502),
(903, 'Credit Card', 199.99, '2024-01-03', 503),
(904, 'Debit Card', 99.99, '2024-01-04', 504),
(905, 'Cash', 39.99, '2024-01-05', 505),
(906, 'Credit Card', 24.99, '2024-01-06', 506),
(907, 'PayPal', 79.99, '2024-01-07', 507),
(908, 'Credit Card', 49.99, '2024-01-08', 508),
(909, 'Debit Card', 19.99, '2024-01-09', 509),
(910, 'Cash', 9.99, '2024-01-10', 510);

-- Insert into shipment
INSERT INTO shipment (shipment_id, method, date, status, address, order_id) VALUES
(1001, 'Standard', '2024-01-01', 'In Transit', 'Cairo, Egypt', 501),
(1002, 'Express', '2024-01-02', 'Delivered', 'Ismailia, Egypt', 502),
(1003, 'Standard', '2024-01-03', 'Delivered', 'Suez, Egypt', 503),
(1004, 'Standard', '2024-01-04', 'In Transit', 'Mansoura, Egypt', 504),
(1005, 'Express', '2024-01-05', 'Delivered', 'Alexandria, Egypt', 505),
(1006, 'Standard', '2024-01-06', 'Delivered', 'Giza, Egypt', 506),
(1007, 'Express', '2024-01-07', 'In Transit', 'Tanta, Egypt', 507),
(1008, 'Standard', '2024-01-08', 'Delivered', 'Hurghada, Egypt', 508),
(1009, 'Express', '2024-01-09', 'In Transit', 'Qena, Egypt', 509),
(1010, 'Standard', '2024-01-10', 'Delivered', 'Sharm El Sheikh, Egypt', 510);

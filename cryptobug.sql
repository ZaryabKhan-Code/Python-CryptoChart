use cryptobug;
create table users(
id int primary key auto_increment,
email varchar (200),
namez varchar (200),
message varchar (1000),
image varchar (2000),
filename varchar (200)
);
desc users;
select * from users;
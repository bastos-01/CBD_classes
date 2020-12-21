# Restaurants DB

## Creating tables

### restaurant

	> create table restaurant(
               ... localidade text,
               ... gastronomia text,
               ... nome text,
               ... restaurant_id int,
               ... primary key (localidade, nome)
               ... ) with clustering order by (nome asc);
               
### 

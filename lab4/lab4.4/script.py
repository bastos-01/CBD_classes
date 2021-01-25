from neo4j import GraphDatabase

class Database:
    def __init__(self):
        self._driver = GraphDatabase.driver("bolt://localhost:7687", auth = ("neo4j", "password"))

    def close(self):
        self._driver.close()

    def insert_nodes(self):
        self._driver.session().run("load csv with headers from 'file:///Users/hacker/Desktop/UA/CBD/CBD_classes/lab4/lab4.4/products_issues.csv' as row with row where row.sub_product is not null merge (p:Product {name: row.product, company: row.company}) merge (sp:SubProduct {name: row.sub_product}) merge (i:Issue {description: row.issue, date: row.date_received})")
        print("Nodes successfully inserted!")

    def insert_relations(self):
        self._driver.session().run("load csv with headers from 'file:///Users/hacker/Desktop/UA/CBD/CBD_classes/lab4/lab4.4/products_issues.csv' as row match (p:Product {name: row.product}) match (sp:SubProduct {name: row.sub_product}) merge (p)-[:HAS]->(sp)")
        self._driver.session().run("load csv with headers from 'file:///Users/hacker/Desktop/UA/CBD/CBD_classes/lab4/lab4.4/products_issues.csv' as row match (i:Issue {description: row.issue, date: row.date_received}) match (p:Product {name: row.product}) merge (i)-[:WRITEN_TO]->(p)")
        print("Relations sucessfully inserted!")
    
    def query(self, query):
        return list(self._driver.session().run(query))
        
    
if __name__ == "__main__":

    # connection established
    connection = Database()

    # Insert data (only executed 1 time)
    #connection.insert_nodes()
    #connection.insert_relations()

    # TODO remove comment of print statements to see the query results

    # query1 - Get all nodes on the database
    query1 = "match(n) return (n)"
    q1 = connection.query(query1)
    #for x in q1:
    #    print(x)

    # query2 - Get the first 20 Products
    query2 = "match(p:Product) return p limit 20"
    q2 = connection.query(query2)
    #for x in q2:
    #    print(x)

    # query3 - Get the first 50 issues and its related products ordered by latest to earliest
    query3 = "match (i:Issue)-[:WRITEN_TO]->(p:Product) return distinct p.name, i.date order by i.date desc limit 50"
    q3 = connection.query(query3)
    #for x in q3:
    #    print(x)

    # query4 - Get the first 30 issues from the 'Mortgage' product ordered by date
    query4 = "match (i:Issue)-[:WRITEN_TO]->(p:Product) where p.name = 'Mortgage' return distinct i order by i.date asc limit 30"
    q4 = connection.query(query4)
    #for x in q4:
    #    print(x)

    # query5 - Get the number of issues in '2012-02-16' from the 'Mortgage' product
    query5 = "match (i:Issue)-[:WRITEN_TO]->(p:Product) where p.name = 'Mortgage' and i.date = '2012-02-16' return count(i) as total_issues"
    q5 = connection.query(query5)
    #for x in q5:
    #    print(x)

    # query6 - Get the total of products that have sub products
    query6 = "match (p:Product)-[:HAS]->(sp:SubProduct) return count(p) as total_products"
    q6 = connection.query(query6)
    #for x in q6:
    #    print(x)

    # query7 - Get all the issues on products of 'Security Credit Services, LLC' company ordered by inverse date
    query7 = "match (i:Issue)-[:WRITEN_TO]->(p:Product) where p.company = 'Security Credit Services, LLC' return distinct p.name, i.description, i.date order by i.date desc"
    q7 = connection.query(query7)
    #for x in q7:
    #    print(x)

    # query8 - Get the number of different dates a issue was writen
    query8 = "match (i:Issue)-[:WRITEN_TO]->(p:Product) return count(distinct i.date) as total_different_dates"
    q8 = connection.query(query8)
    #for x in q8:
    #    print(x)

    # query9 - Get the number of issues from products that have subproducts
    query9 = "match (i:Issue)-[:WRITEN_TO]->(p:Product) match (p:Product)-[:HAS]->(sp:SubProduct) where sp is not null return count(distinct sp) as total_issues_subproducts"
    q9 = connection.query(query9)
    #for x in q9:
    #    print(x)

    # query10 - Get the average text size of the issues writen for the 'Student loan' product
    query10 = "match (i:Issue)-[:WRITEN_TO]->(p:Product) where p.name = 'Student loan' return p.name as Product, avg(size(i.description)) as Issue_Description_Size, count(distinct p) as total_issues"
    q10 = connection.query(query10)
    #for x in q10:
    #    print(x)

    connection.close()

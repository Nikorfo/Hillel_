
----1-----
SELECT name, breed , weight FROM Dogs;

----2----
SELECT name, breed ,weight FROM Dogs
WHERE weight > 25;

----3----
SELECT name, email FROM  Owners
WHERE city = 'Kyiv';

----4----
SELECT name, birth_year FROM Dogs
WHERE breed = 'mixed';

----5----
SELECT reason,visit_date  ,price FROM Visits
ORDER BY price DESC
Limit 5;
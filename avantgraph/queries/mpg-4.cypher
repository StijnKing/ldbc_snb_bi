// 4. Find all people who tagged a company while the company is located in a same country as where they live.
MATCH (m:Post)
        -[cr:hasCreator]->(p:Person)
        -[:isLocatedIn]->(:City)
        -[:isPartOf]->(country:Country { name: "China" }),
    (c:Organisation)-[:isLocatedIn]->(country:Country { name: "China" }),
    (m:Post::(c:Organisation))
WHERE cr.creationDate STARTS WITH "2012"
RETURN p.firstName, p.lastName, c.name, country.name, cr.creationDate;

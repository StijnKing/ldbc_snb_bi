// 4. Find all people who tagged a company while the company is located in a same country as where they live.
MATCH (m:Message::(c:Organisation))
        -[:hasCreator]->(p:Person)
        -[:isLocatedIn]->(:City)
        -[:isPartOf]->(country:Country),
    (c:Organisation)-[:isLocatedIn]->(country:Country)
RETURN p.firstName, p.lastName, c.name, country.name;

// 3. Find all people who tagged a company and the company location while the company is located in a different country than where they live.
MATCH (m:Message::(o:Organisation)-[:isLocatedIn]->(oCountry:Country))
        -[:hasCreator]->(p:Person)
        -[:isLocatedIn]->(:City)
        -[:isPartOf]->(pCountry:Country)
RETURN p.firstName, p.lastName, o.name, oCountry.name, pCountry.name;

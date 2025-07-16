// 11. Query all authors that tagged poeple who mentioned that he or she studied at a university at least 3 times.
MATCH (:Message::(:Message::(c:Person)-[sa:studyAt]->(:University))-[:hasCreator]->(p:Person))-[:hasCreator]->(c)
WITH COUNT(*) AS numTagged, p, c
WHERE numTagged > 2
RETURN p.firstName, p.lastName, c.firstName, c.lastName, numTagged

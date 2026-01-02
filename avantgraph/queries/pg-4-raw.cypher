MATCH (m:Message)-[:hasCreator]->(c:Person)
WITH COUNT(*) AS numTagged, c
WHERE numTagged > 10
RETURN numTagged, c.firstName, c.lastName;

// 9. Find messages that tagged more than 10 people.
MATCH (m:Message::(p:Person))-[:hasCreator]->(c:Person)
WITH COUNT(*) AS numTagged, m, c
WHERE numTagged > 10
RETURN m.content, numTagged, c.firstName, c.lastName;

// 10. Find all university students who tagged someone from a university in CITY_NAME in one of their messages.
MATCH (Message::(p:Person))-[:hasCreator]->(s:Person),
    (p:Person)-[:studyAt]->(u:University)
            -[:isLocatedIn]->(c:City { name: "Maastricht" })
WITH DISTINCT s, u, p
RETURN s.firstName, s.lastName, u.name, p.firstName, p.lastName;

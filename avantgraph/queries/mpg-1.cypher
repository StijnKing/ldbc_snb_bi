// Q1. Find all university students who tagged someone from a university in a different city in one of their messages.
MATCH (:Message::(p:Person))-[:hasCreator]->(s:Person)-[:studyAt]->(uOne:University),
               (p:Person)-[:studyAt]->(uTwo:University)
WHERE NOT uOne = uTwo
RETURN s.firstName, s.lastName, uOne.name, p.firstName, p.lastName, uTwo.name;

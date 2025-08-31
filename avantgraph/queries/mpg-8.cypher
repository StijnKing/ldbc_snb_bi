// 8. Find all knows -> studyAt relationsships that have been mentioned by people in messages.
MATCH (m:Message::(:Person)-[k:knows]->(:Person)-[s:studyAt]->(:University)),
      (p:Person)-[k:knows]->(student:Person)-[s:studyAt]->(u:University)
WITH DISTINCT p, student, u
RETURN p.firstName, p.lastName, student.firstName, student.lastName, u.name;

// 5. Identify all pairs of people who are "friends of friends" (knows someone who knows someone else) and have also interacted by tagging each other in messages.
//     This tests multi-hop relationships and intersection of relationship types.
MATCH (m1:Message::(p1))-[:hasCreator]->(p2),
      (m2:Message::(p2))-[:hasCreator]->(p1),
      (p1:Person)-[:knows]->(:Person)-[:knows]->(p2:Person)
WITH DISTINCT p1, p2
RETURN p1.firstName, p1.lastName, p2.firstName, p2.lastName;

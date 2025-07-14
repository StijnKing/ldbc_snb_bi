// 5. Identify all pairs of people who are "friends of friends" (knows someone who knows someone else) and have also interacted by tagging each other in messages.
//     This tests multi-hop relationships and intersection of relationship types.
// ----- FAILS: Reference missing slot
// TODO: Fix this one
// MATCH (m1:Message::(p1))-[:hasCreator]->(p2),
//       (m2:Message::(p3))-[:hasCreator]->(p4)
//     //   (p1:Person)-[:knows]->(:Person)-[:knows]->(p3:Person)
// WHERE p1 = p4 AND p3 = p2
// RETURN p1.firstName, p1.lastName, p3.firstName, p3.lastName;
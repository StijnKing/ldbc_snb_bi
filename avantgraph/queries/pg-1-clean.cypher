MATCH |l|
WHERE "Message" IN LABELS(l)
RETURN LABELS(l) AS MessageTypes;

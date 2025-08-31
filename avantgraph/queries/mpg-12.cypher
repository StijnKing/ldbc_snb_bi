// 12. How many times is each browser mentioned to be used?
MATCH (:Post)..prop
WHERE KEY(prop) = "browserUsed"
RETURN VALUE(prop), COUNT(VALUE(prop));

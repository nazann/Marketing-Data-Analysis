SELECT 
    c."CustomerID",
    c."CustomerName", 
    c."Email", 
    c."Gender", 
    c."Age", 
    g."Country",
    g."City"
FROM 
    customers AS c  
LEFT JOIN
    geography AS g  
ON 
    c."GeographyID" = g."GeographyID";

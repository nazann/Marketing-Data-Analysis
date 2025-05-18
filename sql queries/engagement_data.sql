select * from engagement_data;


select "EngagementID",
		"ContentID",
		upper(replace("ContentType",'Socialmedia','Social Media')) as "ContentType",
		"Likes",
		split_part("ViewsClicksCombined",'-',1) as "Views",
		split_part("ViewsClicksCombined",'-',2) as "Clicks",
		"CampaignID",
		"ProductID",
		TO_CHAR("EngagementDate"::date, 'DD.MM.YYYY') AS "EngagementDate"

		
		
		from engagement_data;
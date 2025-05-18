SELECT * FROM CUSTOMER_JOURNEY;

with cte as (SELECT "JourneyID",
		"CustomerID",
		"ProductID",
		"VisitDate",
		upper("Stage") as Stage,
		"Action",
		"Duration",
		Avg("Duration") over (partition by "VisitDate")as avg_duration
		,
		row_number() over ( Partition by "CustomerID","ProductID","VisitDate","Stage","Action" order by "JourneyID") as rownum


		from CUSTOMER_JOURNEY
		order by rownum desc) 

select * from cte where rownum=1
order by "VisitDate";


SELECT "JourneyID",
		"CustomerID",
		"ProductID",
		"VisitDate",
		subq.Stage,
		"Action",
		Coalesce("Duration",subq.avg_duration) as "Duration"
		
		from  ( 
		
				SELECT "JourneyID",
				"CustomerID",
				"ProductID",
				"VisitDate",
				upper("Stage") as Stage,
				"Action",
				"Duration",
				Avg("Duration") over (partition by "VisitDate")as avg_duration
				,
				row_number() over ( Partition by "CustomerID","ProductID","VisitDate","Stage","Action" order by "JourneyID") as rownum
		
		
				from CUSTOMER_JOURNEY


		) as subq
		where rownum=1;
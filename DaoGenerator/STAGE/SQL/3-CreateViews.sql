USE sample;
GO


IF (OBJECT_ID (sampleDB., V)) IS NOT NULL 
	DROP VIEW sampleDB.
GO
CREATE VIEW sampleDB.
AS
	SELECT
	
		FORMTYPEID ,		
	
		FORMTYPENAME 		
	
	FROM
	
		FORMTYPE
		
	
	
GO

USE sample;
GO


IF (OBJECT_ID (sampleDB.vFormType, 'V')) IS NOT NULL 
	DROP VIEW sampleDB.vFormType
GO
CREATE VIEW sampleDB.vFormType
AS
	SELECT
	
		FORMTYPEID ,		
	
		FORMTYPENAME 		
	
	FROM
	
		FORMTYPE
		
	
	
GO


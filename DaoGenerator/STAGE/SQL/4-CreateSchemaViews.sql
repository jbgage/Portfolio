USE sample;
GO

IF (OBJECT_ID ('sample.vFormType', 'V')) IS NOT NULL 
	DROP VIEW sample.vFormType 
GO
CREATE VIEW sample.vFormType 
AS 
	SELECT FT.FORMTYPEID , 
		   FT.FORMTYPENAME
	FROM sample.FORMTYPE;
GO


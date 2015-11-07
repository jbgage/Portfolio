USE sample;
GO


IF (OBJECTID(sample.SelectAllSections , 'P')) IS NOT NULL
	DROP PROCEDURE sample.SelectAllSections
GO
CREATE PROCEDURE sample.SelectAllSections
	
		   
	
AS
	BEGIN
		
			SELECT
				
					SECTIONID ,
				
					SECTIONNAME ,
				
					FORMTYPENAME ,
				
					FORMTYPEID 
				
			FROM
				 sample.vSectionType 
			
		
	END;
GO

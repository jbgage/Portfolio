USE sample;
GO
IF  (OBJECT_ID('sample.SECTION_FORMTYPEID_FK' , 'F')) IS NOT NULL
BEGIN
	 ALTER TABLE sample.SECTION
	 DROP CONSTRAINT SECTION_FORMTYPEID_FK;
END;
GO
ALTER TABLE sample.SECTION
ADD CONSTRAINT SECTION_FORMTYPEID_FK
FOREIGN KEY(FORMTYPEID)
REFERENCES sample.FORMTYPE(FORMTYPEID)
GO

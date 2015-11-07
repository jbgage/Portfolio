USE sampleDB;
GO

IF OBJECT_ID('sample.FORMTYPEID_FK' , 'F') IS NOT NULL
BEGIN
	ALTER TABLE sample.SECTION
	DROP CONSTRAINT FORMTYPEID_FK
END

ALTER TABLE sample.SECTION
ADD CONSTRAINT FORMTYPEID_FK
FOREIGN KEY (FORMTYPEID)
REFERENCES FORMTYPE.FORMTYPEID;
GO


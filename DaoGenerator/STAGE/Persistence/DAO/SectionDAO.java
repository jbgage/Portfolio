package app.persistence.dao;
import java.util.List;
import app.model;

	/****************************************************************
	-  This is the DAO to manage access to the SECTION table and views
	****************************************************************/

public interface SectionDAO {
		 List<SectionModel> SelectSectionsByFormTypeId (  int SectionTypeId  ) ;
		 SectionModel SelectSectionBySectionId (  int SectionId  ) ;
}

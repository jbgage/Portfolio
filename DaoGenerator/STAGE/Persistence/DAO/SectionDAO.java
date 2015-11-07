package app.persistence.dao;
import java.util.List;
import app.model;

/****************************************************************
This is the DAO to manage access to the SECTION table and views
*****************************************************************/

public interface SectionDAO {
	
	public List<SectionModel> SelectAllSections ();
	
	public List<SectionModel> SelectSectionsByFormTypeId ();
	
	public SectionModel SelectSectionBySectionId ();
	
}
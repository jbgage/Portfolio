package app.model;
import java.util.Serializable;

public class SectionModel implements Serializable {

	
	private int SectionId;
	
	private String SectionName;
	
	private int FormTypeId;
	
	private String FormTypeName;
	

	public (){
	}
	
	
	public  int getSectionid(){
		return SectionId
	}
	
	public void setSectionid(int SectionId){
		this.SectionId = SectionId;
	}
	
	public  String getSectionname(){
		return SectionName
	}
	
	public void setSectionname(String SectionName){
		this.SectionName = SectionName;
	}
	
	public  int getFormtypeid(){
		return FormTypeId
	}
	
	public void setFormtypeid(int FormTypeId){
		this.FormTypeId = FormTypeId;
	}
	
	public  String getFormtypename(){
		return FormTypeName
	}
	
	public void setFormtypename(String FormTypeName){
		this.FormTypeName = FormTypeName;
	}
	
}
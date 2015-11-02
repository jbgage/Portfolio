package app.model; 

import java.util.Serializable;

public class SectionModel implements Serializable
{
		private int SectionId;
		private String SectionName;
		private int FormTypeId;
		private String FormTypeName;
		public SectionModel() {
		}
		public int getSectionId(){
				return SectionId;
		}
		public String getSectionName(){
				return SectionName;
		}
		public int getFormTypeId(){
				return FormTypeId;
		}
		public String getFormTypeName(){
				return FormTypeName;
		}
		public void setSectionId(int SectionId){
				this.SectionId = SectionId;
		}
		public void setSectionName(String SectionName){
				this.SectionName = SectionName;
		}
		public void setFormTypeId(int FormTypeId){
				this.FormTypeId = FormTypeId;
		}
		public void setFormTypeName(String FormTypeName){
				this.FormTypeName = FormTypeName;
		}
}

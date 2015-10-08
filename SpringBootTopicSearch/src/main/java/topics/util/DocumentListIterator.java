package topics.util;
import java.util.List;
import java.util.Iterator;
import java.util.Arrays;
import java.net.URI;
import cc.mallet.types.Instance;
import topics.model.DocumentValueObject;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DocumentListIterator implements Iterator<Instance>{
	
	private Logger logger = LoggerFactory.getLogger(DocumentListIterator.class.getName());
	
	private Iterator<DocumentValueObject> subIterator;
	private DocumentValueObject target;
	private int index;
		
	public DocumentListIterator(List<DocumentValueObject> data , DocumentValueObject target){
		this.subIterator = data.iterator();
		this.target = target;
		this.index=0;
	}
	
	public DocumentListIterator(List<DocumentValueObject> data){
		this(data , null);
	}
	
	public DocumentListIterator(DocumentValueObject[] data , DocumentValueObject target){
		this(Arrays.asList(data) , target);
	}
	
	public DocumentListIterator(DocumentValueObject[] data){
		this(data , null);
	}
	
	public Instance next(){ 
		URI uri = null;
		try{
			uri = new URI("array:" + this.index++);
		
		} catch (Exception e){
			logger.error("Exception occurred - {}" , e.getMessage());
			throw new IllegalStateException();
		}
		return new Instance( this.subIterator.next() , this.target , uri , null);
	}
	
	public boolean hasNext(){
		return this.subIterator.hasNext();
	}
	
	public void remove(){
		this.subIterator.remove();
	}

}

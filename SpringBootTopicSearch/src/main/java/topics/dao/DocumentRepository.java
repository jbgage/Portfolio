package topics.dao;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;
import org.springframework.stereotype.Repository;

import topics.model.DocumentValueObject;

import java.util.List;

@Repository("documentRepository")
public interface DocumentRepository extends ElasticsearchRepository<DocumentValueObject , String>{
	public List<DocumentValueObject> findByKeyword(String keyword);	
}

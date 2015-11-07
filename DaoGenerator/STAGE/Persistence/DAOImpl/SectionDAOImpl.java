package app.persistence.dao.daoImpl;
import java.util.List;
import java util.LinkedList;
import java.util.HashMap;
import javax.annotation.Resource;
import org.apache.tomcat.jdbc.pool.DataSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.simple.SimpleJdbcCall;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import app.model.*;
import app.persistence.dao.SectionDAO;

/**************************************************
This DAOImpl performs CRUD operations on the view and table relevant to SECTIONs and implements the DAO: SectionDAO 
***************************************************/

public class SectionDAOImpl implements SectionDAO {
	
	private Logger logger = LoggerFactory.getLogger(SectionDAOImpl.class.getName();
	
	@Autowired
    @Resource(name="jdbcTemplate")
    private JdbcTemplate jdbcTemplate; 
        
    @Autowired 
    @Resource(name="dataSource") 
    private DataSource dataSource;   
    
    public SectionDAOImpl (){
    }
    
    
    
    public List <SectionModel> GetSectionsByTypeId () {
    	List <SectionModel> list = null;
    	try{
    		list = new List<SectionModel>();
    		SimpleJdbcCall jdbcCall = new SimpleJdbcCall(jdbcTemplate)		
    											.withProcedureName(sample.SelectSectionsByTypeId)
    											.returningResultSet(SectionModel , BeanPropertyRowMapper.newInstance(SectionModel.class));
    		Map map = jdbcCall.execute(new HashMap<String , Object>(0));
    		list = (List) m.get("SectionModel");
    	} catch(Exception ex){
    		logger.logger("******************* SectionDAOImpl.GetSectionsByTypeId: Error occurred - {0}" , ex.getMessage());
    	}
    	return list;
    }
 

}
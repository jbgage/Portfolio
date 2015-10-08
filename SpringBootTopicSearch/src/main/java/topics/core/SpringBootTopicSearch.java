package topics.core;
import topics.dao.DocumentRepository;
import topics.model.DocumentValueObject;
import topics.util.TopicModellingUtility;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import java.util.List;
import java.util.Scanner;

@SpringBootApplication
@ComponentScan(basePackages={"topics"})
public class SpringBootTopicSearch implements CommandLineRunner {
	
	@Autowired
	@Qualifier("documentRepository")
	private DocumentRepository dao;
	
	@Autowired
	@Qualifier("topicModellingUtility")
	private TopicModellingUtility topicModel;
	
	private static final Logger logger = LoggerFactory.getLogger(SpringBootTopicSearch.class.getName());
	
	@Override
	public void run(String... args) throws Exception{
		String topics = "";
		try(Scanner scanner = new Scanner(System.in)){
			logger.info("Enter a term:");
			String searchTerm = scanner.nextLine();
			logger.info("Enter number of topics:");
			String numTopics = scanner.nextLine();
			logger.info("Enter a rank level:");
			String rankLevel = scanner.nextLine();
			if (((numTopics != null) && (numTopics.length() > 0)) && ((rankLevel != null) && (rankLevel.length() > 0))){
				int iNumTopics = Integer.parseInt(numTopics);
				int iRankLevel = Integer.parseInt(rankLevel);
				if (this.dao.findByKeyword(searchTerm) != null){
					List<DocumentValueObject> list = this.dao.findByKeyword(searchTerm);
					topics = this.topicModel.getTopics(list, iNumTopics, iRankLevel);
					logger.info("Topics = {}" , topics);
				}
			}
		}
		catch(Exception ex){
			logger.error("Error occurred - {}" , ex.getMessage());
		}
	}
	
	public static void main(String... args){
		SpringApplication.run(SpringBootTopicSearch.class, "--debug").close();
	}
}

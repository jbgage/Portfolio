package topics.util;

import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.TreeSet;
import java.util.regex.Pattern;

import cc.mallet.pipe.CharSequence2TokenSequence;
import cc.mallet.pipe.CharSequenceLowercase;
import cc.mallet.pipe.Pipe;
import cc.mallet.pipe.SerialPipes;
import cc.mallet.pipe.TokenSequence2FeatureSequence;
import cc.mallet.topics.ParallelTopicModel;
import cc.mallet.types.Alphabet;
import cc.mallet.types.IDSorter;
import cc.mallet.types.InstanceList;
import topics.model.DocumentValueObject;

import java.util.Iterator;

import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.slf4j.Logger;

@Component("topicModellingUtility")
public class TopicModellingUtility {
	
	private Logger logger = LoggerFactory.getLogger(TopicModellingUtility.class.getName());
	
	public String getTopics(List<DocumentValueObject> list , int numTopics , int maxRank){
		ArrayList<Pipe> pipeList = new ArrayList<Pipe>();
		String ls = System.getProperty("line.separator");
		StringBuilder sb = new StringBuilder();
		try{
			pipeList.add( new CharSequenceLowercase() );
	        pipeList.add( new CharSequence2TokenSequence(Pattern.compile("\\p{L}[\\p{L}\\p{P}]+\\p{L}")) );
	        pipeList.add( new TokenSequence2FeatureSequence() );
	        InstanceList instances = new InstanceList(new SerialPipes(pipeList));
	        instances.addThruPipe(new DocumentListIterator(list));
	        ParallelTopicModel model = new ParallelTopicModel(numTopics , 1.0 , 0.01);
	        model.addInstances(instances);
	        model.setNumThreads(2);
	        model.setNumIterations(50);
	        model.estimate();
	        Alphabet dataAlphabet = instances.getDataAlphabet();
	        double[] topicDistribution = model.getTopicProbabilities(0);
	        ArrayList<TreeSet<IDSorter>> topicSortedWords = model.getSortedWords();
	        int rank = 0;
	        for (int topic=0; topic < numTopics ; topic++){
	        	Iterator<IDSorter> iterator = topicSortedWords.get(topic).iterator();
	        	sb.append(MessageFormat.format("Topic Number: {0} = {1}.", topic , topicDistribution[topic])).append(ls);
	        	while (iterator.hasNext() && rank < maxRank){
	        		IDSorter idCountPair = iterator.next();
	        		sb.append(MessageFormat.format("Topic Lookup: {0} - ({1}).", dataAlphabet.lookupObject(idCountPair.getID()) , idCountPair.getWeight())).append(ls);
	        		rank++;
	        	}
	        }
		} catch (Exception ex){
			logger.error("Error occurred - {}" , ex.getMessage());
		}
		return sb.toString();
	}

}

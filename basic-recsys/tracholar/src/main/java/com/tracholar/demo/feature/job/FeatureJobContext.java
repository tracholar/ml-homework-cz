package com.tracholar.demo.feature.job;

import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.feature.IFeatureJob;
import com.tracholar.demo.feature.dag.IEngineContext;
import com.tracholar.demo.feature.job.global.GlobalJobResults;
import com.tracholar.demo.feature.job.item.ItemJobResults;
import lombok.Getter;
import lombok.Setter;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/10/1 15:18
 */
public class FeatureJobContext implements
        IEngineContext<IFeatureJob, IJobResults> {
    @Getter
    @Setter
    private long uid;

    @Getter
    @Setter
    private List<IEngineItem> items = new LinkedList<>();


    private Map<IFeatureJob, IJobResults> results = new HashMap<>();

    @Override
    public boolean isExecuted(IFeatureJob node) {
        return results.containsKey(node);
    }

    @Override
    public void addFinishedNode(IFeatureJob node, IJobResults value) {
        results.put(node, value);
    }

    /**
     * 按Job返回输出结果
     * @return
     */
    public Map<IFeatureJob, IJobResults> getOutputs(){
        return results;
    }

    public JobEngineResults getResults(){
        JobEngineResults results = new JobEngineResults();
        GlobalJobResults globalJobResults = new GlobalJobResults();
        ItemJobResults itemJobResults = new ItemJobResults();
        for(IJobResults r : this.results.values()){
            if(r instanceof GlobalJobResults){
                globalJobResults.merge((GlobalJobResults) r);
            }else if(r instanceof ItemJobResults){
                itemJobResults.merge((ItemJobResults) r);
            }else{
                // TODO 待解决
            }
        }
        results.setGlobalJobResults(globalJobResults);
        results.setItemJobResults(itemJobResults);
        return results;
    }
}

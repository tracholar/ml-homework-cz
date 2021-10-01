package com.tracholar.demo.feature.job.global;

import com.tracholar.demo.data.FeatureEntity;
import com.tracholar.demo.data.FeatureEntityRepository;
import com.tracholar.demo.engine.engine.EngineItemType;
import com.tracholar.demo.feature.IFeatureJob;
import com.tracholar.demo.feature.dag.INode;
import com.tracholar.demo.feature.job.FeatureJobContext;
import com.tracholar.demo.feature.job.IGlobalJob;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Arrays;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/10/1 15:07
 */
@Component
public class UserBaseFeatureJob implements IGlobalJob {
    @Override
    public List<String> getDependence() {
        return null;
    }

    @Override
    public void addDependence(IFeatureJob job) {

    }

    @Override
    public List<INode> getDependenceNode() {
        return null;
    }

    @Getter
    private List<String> outputNames = Arrays.asList(
            "USER_CLICK_LIST",
            "USER_COLLECT_LIST"
    );

    @Autowired
    private FeatureEntityRepository rep;

    @Override
    public GlobalJobResults run(FeatureJobContext ctx) {
        long uid = ctx.getUid();
        List<FeatureEntity> data = rep.findFeature(EngineItemType.USER.getId(), Arrays.asList(uid), outputNames);

        GlobalJobResults results = new GlobalJobResults();
        for(FeatureEntity e : data){
            results.put(e.getName(), e.getValue());
        }

        return results;
    }
}

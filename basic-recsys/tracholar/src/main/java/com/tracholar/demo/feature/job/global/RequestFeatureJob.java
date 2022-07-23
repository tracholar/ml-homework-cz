package com.tracholar.demo.feature.job.global;

import com.tracholar.demo.feature.IFeatureJob;
import com.tracholar.demo.feature.dag.INode;
import com.tracholar.demo.feature.job.FeatureJobContext;
import com.tracholar.demo.feature.job.IGlobalJob;
import lombok.Getter;
import org.springframework.stereotype.Component;

import java.util.*;

/**
 * @author zuoyuan
 * @date 2021/10/1 12:32
 */
@Component
public class RequestFeatureJob implements IGlobalJob {
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
    private List<String> outputNames = Arrays.asList(F_UID);
    private final static String F_UID = "UID";

    @Override
    public GlobalJobResults run(FeatureJobContext ctx) {
        GlobalJobResults output = new GlobalJobResults();
        output.put(F_UID, ctx.getUid());

        return output;
    }
}

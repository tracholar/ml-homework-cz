package com.tracholar.demo.feature.service;

import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.feature.FeatureServiceRequest;
import com.tracholar.demo.feature.IFeatureService;
import com.tracholar.demo.feature.job.JobEngineResults;
import com.tracholar.demo.feature.job.JobExecuteEngine;
import com.tracholar.demo.feature.job.item.ItemJobResults;
import com.tracholar.demo.model.Sample;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.*;

/**
 * @author zuoyuan
 * @date 2021/9/29 20:56
 */
@Component
public class SimpleFeatureService implements IFeatureService {
    @Autowired
    private JobExecuteEngine engine;

    @Override
    public List<Sample> getFeatures(FeatureServiceRequest req) {
        List<Sample> samples = new LinkedList<>();

        JobEngineResults results = engine.run(req.buildFeatureJobContext());

        for(IEngineItem item : req.getItems()){
            Sample s = new Sample();
            s.setReqId(req.getReq().getReqId());
            s.setUid(req.getReq().getUid());
            s.setType(item.getType());
            s.setId(item.getId());

            // 特征
            Map<String, Object> features = new HashMap<>();
            features.putAll(results.getGlobalJobResults());
            features.putAll(results.getItemJobResults().getOrDefault(item, Collections.emptyMap()));
            s.setFeatures(features);

            samples.add(s);
        }
        return samples;
    }
}

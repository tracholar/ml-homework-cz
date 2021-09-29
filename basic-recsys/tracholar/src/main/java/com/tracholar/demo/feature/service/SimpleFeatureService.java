package com.tracholar.demo.feature.service;

import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.feature.FeatureServiceRequest;
import com.tracholar.demo.feature.IFeatureService;
import com.tracholar.demo.model.Sample;

import java.util.LinkedList;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 20:56
 */
public class SimpleFeatureService implements IFeatureService {
    @Override
    public List<Sample> getFeatures(FeatureServiceRequest req) {
        List<IEngineItem> items = req.getItems();
        List<Sample> samples = new LinkedList<>();

        for(int i = 0; i < items.size(); i++){
            Sample s = new Sample();
            s.setId(i);
            s.setFeatures(new LinkedList<>());

            samples.add(s);
        }
        return samples;
    }
}

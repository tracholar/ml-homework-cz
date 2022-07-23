package com.tracholar.demo.engine.rank.ranker;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.engine.rank.IRanker;
import com.tracholar.demo.feature.FeatureServiceRequest;
import com.tracholar.demo.feature.IFeature;
import com.tracholar.demo.feature.IFeatureService;
import com.tracholar.demo.feature.service.SimpleFeatureService;
import com.tracholar.demo.model.*;
import com.tracholar.demo.model.model.RandomModel;
import lombok.Builder;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/29 20:21
 */
public class SimpleModelRanker implements IRanker {
    @Setter
    private IPredictor model;
    @Autowired
    private IFeatureService service;

    @Override
    public List<IEngineItem> rank(List<IEngineItem> items, EngineRequest request) {
        FeatureServiceRequest req = FeatureServiceRequest.builder()
                .items(items).req(request).build();
        List<Sample> samples = service.getFeatures(req);
        PredictRequest predReq = PredictRequest.builder().items(samples).build();
        IPredictResponse resp = model.predict(predReq);
        Map<String, PredictResult> predResults = resp.getResults();
        for(Sample s : samples){
            PredictResult pred = predResults.get(s.getUniqueId());
            IEngineItem item = s.getItem();
            item.setScore(pred.getScore());
        }
        items.sort((o1, o2) -> -Float.compare(o1.getScore(),o2.getScore()));
        return items;
    }
}

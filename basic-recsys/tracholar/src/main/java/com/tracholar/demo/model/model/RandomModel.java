package com.tracholar.demo.model.model;

import com.tracholar.demo.model.*;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/29 20:26
 */
@Component
public class RandomModel implements IPredictor {

    @Override
    public IPredictResponse predict(IPredictRequest request) {
        List<Sample> items = request.getItems();
        Map<String, PredictResult> results = new HashMap<>();
        for(Sample s : items){
            PredictResult result = PredictResult.builder()
                    .id(s.getId())
                    .score((float)Math.random())
                    .build();
            results.put(s.getUniqueId(), result);
        }

        return PredictResponse.builder().results(results)
                .build();
    }
}

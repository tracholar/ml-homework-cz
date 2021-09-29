package com.tracholar.demo.model.model;

import com.tracholar.demo.model.*;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/29 20:26
 */
public class RandomModel implements IPredictor {

    @Override
    public IPredictResponse predict(IPredictRequest request) {
        List<Sample> items = request.getItems();
        Map<Integer, PredictResult> results = new HashMap<>();
        for(int i=0; i<items.size(); i++){
            Sample s = items.get(i);
            PredictResult result = PredictResult.builder()
                    .id(s.getId())
                    .score((float)Math.random())
                    .build();
            results.put(i, result);
        }

        return PredictResponse.builder().results(results)
                .build();
    }
}

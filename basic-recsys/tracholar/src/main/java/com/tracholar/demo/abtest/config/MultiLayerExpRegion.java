package com.tracholar.demo.abtest.config;

import com.tracholar.demo.abtest.ABTestInfo;
import lombok.Data;

import java.util.List;
import java.util.Set;

/**
 * @author zuoyuan
 * @date 2021/10/3 11:21
 */
@Data
public class MultiLayerExpRegion extends LayerConfig implements IExpRegion{
    private Set<Integer> flows;
    private List<String> layerKeys;

    @Override
    public ABTestInfo genABTestInfo(String flowId, int bucketNum) {
        ABTestInfo info = new ABTestInfo();
        String strategyName = findMatchStrategy(flowId, bucketNum);
        for(String layer : layerKeys){
            info.put(layer, strategyName);
        }
        return info;
    }
}

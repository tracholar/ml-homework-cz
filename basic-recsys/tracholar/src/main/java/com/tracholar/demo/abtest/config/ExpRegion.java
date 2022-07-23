package com.tracholar.demo.abtest.config;

import com.tracholar.demo.abtest.ABTestInfo;
import lombok.Data;

import java.util.List;
import java.util.Set;

/**
 * @author zuoyuan
 * @date 2021/10/2 16:07
 */
@Data
public class ExpRegion implements IExpRegion{
    private String name;
    private Set<Integer> flows;
    private List<LayerConfig> configs;
    private String desc;


    @Override
    public ABTestInfo genABTestInfo(String flowId, int bucketNum) {
        // 各层实验
        ABTestInfo info = new ABTestInfo();
        for(LayerConfig c : getConfigs()){
            String strategyName = c.findMatchStrategy(flowId, bucketNum);
            info.put(c.getLayerName(), strategyName);
        }
        return info;
    }
}

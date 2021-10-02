package com.tracholar.demo.abtest;

import com.google.gson.Gson;
import com.tracholar.demo.abtest.config.ABTestConfig;
import com.tracholar.demo.abtest.config.ExpRegion;
import com.tracholar.demo.abtest.config.LayerConfig;
import com.tracholar.demo.abtest.config.StrategyConfig;
import org.springframework.stereotype.Component;

import java.io.InputStreamReader;
import java.io.Reader;

/**
 * @author zuoyuan
 * @date 2021/10/2 15:44
 */
@Component
public class ABTestService implements IABTest{
    private ABTestConfig config;
    public ABTestService(){
        Gson gson = new Gson();
        Reader reader = new InputStreamReader(getClass().getResourceAsStream("/abtest.json"));
        config = gson.fromJson(reader, ABTestConfig.class);
    }

    private int hash(String flowId, int seed){
        int code = flowId.hashCode();
        if(code < 0){
            code = - code;
        }
        return code % 100;
    }

    @Override
    public IABTestInfo getABTestInfo(String flowId) {
        ABTestInfo info = new ABTestInfo();
        if(flowId == null){
            return info;
        }
        int flow = hash(flowId, config.getSeed());

        // 试验区，默认是正交实验区
        ExpRegion hitRegion = config.getRegions().get(1);
        for(ExpRegion region : config.getRegions()){
            if(region.getFlows().contains(flow)){
                hitRegion = region;
                break;
            }
        }

        // 各层实验
        for(LayerConfig c : hitRegion.getConfigs()){
            flow = hash(flowId, c.getSeed());
            for(StrategyConfig sc : c.getConfigs()){
                if(sc.getFlows().contains(flow)){
                    info.put(c.getLayerName(), sc.getStrategyName());
                }
            }
        }
        return info;
    }
}

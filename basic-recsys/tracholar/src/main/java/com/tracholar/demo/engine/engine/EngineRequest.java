package com.tracholar.demo.engine.engine;

import com.tracholar.demo.abtest.IABTestInfo;
import lombok.Builder;
import lombok.Getter;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:51
 */
@Builder
public class EngineRequest {
    @Getter
    private String reqId;

    @Getter
    private long uid;
    @Getter
    private int limitSize;

    private IABTestInfo abTestInfo;

    public String getRecallerKey(){
        return abTestInfo.getLayerKey("recall");
    }

    public String getRecallFilterKey(){
        return abTestInfo.getLayerKey("recallFilter");
    }

    public String getRankerKey(){
        return abTestInfo.getLayerKey("ranker");
    }

    public String getRankFilterKey(){
        return abTestInfo.getLayerKey("rankFilter");
    }
}

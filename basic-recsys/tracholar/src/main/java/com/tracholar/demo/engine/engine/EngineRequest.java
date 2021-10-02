package com.tracholar.demo.engine.engine;

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

    public String getRecallerKey(){
        return "default";
    }

    public String getRecallFilterKey(){
        return "default";
    }

    public String getRankerKey(){
        return "base";
    }

    public String getRankFilterKey(){
        return "default";
    }
}

package com.tracholar.demo.engine.filter;

import com.tracholar.demo.engine.engine.EngineRequest;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:41
 */
public class RecallFilter extends FilterRouter{

    @Override
    protected String getExpKey(EngineRequest request) {
        return request.getRecallFilterKey();
    }
}

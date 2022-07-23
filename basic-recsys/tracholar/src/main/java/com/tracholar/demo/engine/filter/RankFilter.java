package com.tracholar.demo.engine.filter;

import com.tracholar.demo.engine.engine.EngineRequest;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:42
 */
public class RankFilter extends FilterRouter{
    @Override
    protected String getExpKey(EngineRequest request) {
        return request.getRankFilterKey();
    }
}

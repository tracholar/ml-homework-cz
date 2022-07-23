package com.tracholar.demo.engine.engine;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:48
 *
 * 推荐引擎
 */
public interface IEngine {
    /**
     * 推荐引擎接口
     * @param request
     * @return
     */
    EngineResponse recommend(EngineRequest request);
}

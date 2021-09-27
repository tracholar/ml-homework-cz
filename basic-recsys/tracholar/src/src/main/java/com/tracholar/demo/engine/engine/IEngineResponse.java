package com.tracholar.demo.engine.engine;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:49
 */
public interface IEngineResponse {
    /**
     * 引擎返回的结果
     * @return
     */
    List<IEngineItem> getResults();
}

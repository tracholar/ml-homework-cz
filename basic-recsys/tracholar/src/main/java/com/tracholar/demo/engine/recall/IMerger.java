package com.tracholar.demo.engine.recall;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;

import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/29 17:59
 *
 * 多路召回融合
 */
public interface IMerger {
    /**
     * 融合多路召回结果
     * @param results
     * @param request
     * @return
     */
    List<IEngineItem> merge(Map<IRecaller, List<IEngineItem>> results, EngineRequest request);
}

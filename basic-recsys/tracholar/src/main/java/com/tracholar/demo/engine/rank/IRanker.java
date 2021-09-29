package com.tracholar.demo.engine.rank;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 17:40
 */
public interface IRanker {
    /**
     * 排序接口
     * @param items
     * @param request
     * @return
     */
    List<IEngineItem> rank(List<IEngineItem> items, EngineRequest request);
}

package com.tracholar.demo.engine.filter;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:30
 *
 * 召回和排序后的过滤逻辑
 */
public interface IFilter {
    /**
     * 过滤逻辑
     * @param items
     * @param request
     * @return
     */
    List<IEngineItem> filter(List<IEngineItem> items, EngineRequest request);
}

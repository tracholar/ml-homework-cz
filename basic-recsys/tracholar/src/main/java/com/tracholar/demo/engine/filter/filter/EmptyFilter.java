package com.tracholar.demo.engine.filter.filter;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.engine.filter.FilterFactory;
import com.tracholar.demo.engine.filter.IFilter;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:42
 */
public class EmptyFilter implements IFilter {
    @Override
    public List<IEngineItem> filter(List<IEngineItem> items, EngineRequest request) {
        return items;
    }

    private static IFilter emptyFilter = new EmptyFilter();

    public static IFilter getInstance(){
        return emptyFilter;
    }
}

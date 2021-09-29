package com.tracholar.demo.engine.filter;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;

import java.util.LinkedList;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:33
 */
public class FilterList implements IFilter{
    private List<IFilter> filters = new LinkedList<>();

    @Override
    public List<IEngineItem> filter(List<IEngineItem> items, EngineRequest request) {
        for(IFilter f : filters){
            items = f.filter(items, request);
        }
        return items;
    }
}

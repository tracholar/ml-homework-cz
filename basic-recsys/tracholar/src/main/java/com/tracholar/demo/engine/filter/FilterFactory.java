package com.tracholar.demo.engine.filter;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:39
 */
public class FilterFactory {
    public static class EmptyFilter implements IFilter{
        @Override
        public List<IEngineItem> filter(List<IEngineItem> items, EngineRequest request) {
            return items;
        }
    }

    private static IFilter emptyFilter = new EmptyFilter();

    public IFilter getEmptyFilter(){
        return emptyFilter;
    }
}

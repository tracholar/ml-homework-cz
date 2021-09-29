package com.tracholar.demo.engine.filter;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.engine.filter.filter.EmptyFilter;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:32
 */
public abstract class FilterRouter implements IFilter{
    private Map<String, IFilter> routers = new HashMap<>();
    private IFilter defaultFilter = EmptyFilter.getInstance();

    /**
     * 获取实验key
     * @return
     */
    protected abstract String getExpKey(EngineRequest request);

    @Override
    public List<IEngineItem> filter(List<IEngineItem> items, EngineRequest request) {
        String key = getExpKey(request);
        IFilter f = routers.get(key);
        f = f == null ? defaultFilter : f;

        return f.filter(items, request);
    }
}

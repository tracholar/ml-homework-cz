package com.tracholar.demo.engine.rank;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.engine.rank.ranker.SimpleModelRanker;
import com.tracholar.demo.engine.rank.ranker.SimpleRanker;
import com.tracholar.demo.utils.Monitor;
import lombok.Data;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/29 17:46
 *
 * ranker的路由，用于AB实验
 */
@Data
public class RankerRouter implements IRanker{
    private IRanker defaultRanker = new SimpleModelRanker();
    private Map<String, IRanker> routerTable = new HashMap<>();

    @Override
    public List<IEngineItem> rank(List<IEngineItem> items, EngineRequest request) {
        IRanker ranker = routerTable.get(request.getRankerKey());
        ranker = ranker == null ? defaultRanker : ranker;

        Monitor.log("RankerRouter", ranker.getClass().getSimpleName());
        return ranker.rank(items, request);
    }
}

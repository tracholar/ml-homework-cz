package com.tracholar.demo.engine.engine;

import com.tracholar.demo.engine.filter.IFilter;
import com.tracholar.demo.engine.filter.RankFilter;
import com.tracholar.demo.engine.filter.RecallFilter;
import com.tracholar.demo.engine.rank.IRanker;
import com.tracholar.demo.engine.rank.RankerRouter;
import com.tracholar.demo.engine.recall.IRecaller;
import com.tracholar.demo.engine.recall.RecallerRouter;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:36
 */
@Component
public class SimpleRecEngine implements IEngine{
    @Resource(name = "recall_router")
    private IRecaller recaller;
    private IFilter recallFilter = new RecallFilter();
    @Resource(name = "ranker_router")
    private IRanker ranker;
    private IFilter rankFilter = new RankFilter();

    @Override
    public EngineResponse recommend(EngineRequest request) {
        List<IEngineItem> items = recaller.recall(request);
        items = recallFilter.filter(items, request);
        items = ranker.rank(items, request);
        items = rankFilter.filter(items, request);

        EngineResponse response = EngineResponse.builder()
                .items(items)
                .build();
        return response;
    }
}

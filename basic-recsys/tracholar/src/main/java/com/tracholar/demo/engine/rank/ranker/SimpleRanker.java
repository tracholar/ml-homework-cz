package com.tracholar.demo.engine.rank.ranker;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.engine.rank.IRanker;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 17:42
 *
 * 用召回分数排序
 */
public class SimpleRanker implements IRanker {
    @Override
    public List<IEngineItem> rank(List<IEngineItem> items, EngineRequest request) {
        items.sort((o1, o2) -> -Float.compare(o1.getScore(), o2.getScore()));
        return items;
    }
}

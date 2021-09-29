package com.tracholar.demo.engine.recall.strategy;

import com.tracholar.demo.data.InvertIndex;
import com.tracholar.demo.data.InvertIndexEntity;
import com.tracholar.demo.data.InvertIndexEntityRepository;
import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.engine.recall.IRecaller;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 15:25
 */
@Component
public class SimpleRecaller implements IRecaller {
    @Autowired
    private InvertIndexEntityRepository repository;

    private static String key = "toplist";
    @Override
    public List<IEngineItem> recall(EngineRequest request) {
        // 热门召回
        InvertIndexEntity index = repository.findById(key).get();
        return index.getData().toItems();
    }
}

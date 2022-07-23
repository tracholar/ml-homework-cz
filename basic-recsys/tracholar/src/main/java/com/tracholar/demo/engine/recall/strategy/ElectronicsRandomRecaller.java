package com.tracholar.demo.engine.recall.strategy;

import com.tracholar.demo.data.ArticleRepository;
import com.tracholar.demo.data.amazon.ElectronicsRepository;
import com.tracholar.demo.engine.engine.EngineItemType;
import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.GeneralEngineItem;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.engine.recall.IRecaller;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.LinkedList;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/10/4 12:03
 */
@Component
public class ElectronicsRandomRecaller implements IRecaller {
    @Autowired
    private ElectronicsRepository rep;

    @Override
    public List<IEngineItem> recall(EngineRequest request) {
        List<IEngineItem> r = new LinkedList<>();
        rep.sample().forEach(e -> {
            GeneralEngineItem item = new GeneralEngineItem();
            item.setType(EngineItemType.ELECTRONICS);
            item.setId(e.getId());
            item.setScore((float) Math.random());
            r.add(item);
        });
        return r;
    }
}

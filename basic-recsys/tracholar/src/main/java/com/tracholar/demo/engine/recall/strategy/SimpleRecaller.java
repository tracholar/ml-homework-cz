package com.tracholar.demo.engine.recall.strategy;

import com.tracholar.demo.data.InvertIndex;
import com.tracholar.demo.data.InvertIndexEntity;
import com.tracholar.demo.data.InvertIndexEntityRepository;
import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.engine.recall.IRecaller;
import lombok.Data;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Configurable;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 15:25
 */
@Setter
public class SimpleRecaller implements IRecaller {
    @Autowired
    private InvertIndexEntityRepository repository;

    private String key;

    public SimpleRecaller(String key){
        this.key = key;
    }

    @Override
    public List<IEngineItem> recall(EngineRequest request) {
        // 热门召回
        InvertIndexEntity index = repository.findById(key).get();
        return index.getData().toItems();
    }
}

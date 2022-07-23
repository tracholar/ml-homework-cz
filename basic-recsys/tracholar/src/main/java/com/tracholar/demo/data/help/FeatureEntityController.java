package com.tracholar.demo.data.help;

import com.tracholar.demo.data.FeatureEntity;
import com.tracholar.demo.data.FeatureEntityRepository;
import com.tracholar.demo.data.amazon.Electronics;
import com.tracholar.demo.engine.engine.EngineItemType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.LinkedList;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/10/2 09:15
 *
 * 特征生产
 */
@RestController
@RequestMapping("/feature")
public class FeatureEntityController {
    @Autowired
    private FeatureEntityRepository rep;
    @RequestMapping("/mock")
    public FeatureEntity mock(){
        FeatureEntity e = new FeatureEntity(0, (short) EngineItemType.ELECTRONICS.getId(),
                5L, "ITEM_INFO", "{\"CNT\":10}");
        return rep.save(e);
    }

    @RequestMapping("/list")
    public Iterable<FeatureEntity> list(){
        return rep.findAll();
    }

}

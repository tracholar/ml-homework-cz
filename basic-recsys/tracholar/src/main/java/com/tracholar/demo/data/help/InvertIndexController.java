package com.tracholar.demo.data.help;

import com.tracholar.demo.data.InvertIndex;
import com.tracholar.demo.data.InvertIndexEntity;
import com.tracholar.demo.data.InvertIndexEntityRepository;
import com.tracholar.demo.data.amazon.Electronics;
import com.tracholar.demo.data.amazon.ElectronicsRepository;
import com.tracholar.demo.engine.engine.EngineItemType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/30 15:32
 */
@RestController
@RequestMapping("/invertIndex")
public class InvertIndexController {
    @Autowired
    private InvertIndexEntityRepository repository;
    @Autowired
    private ElectronicsRepository elecRep;

    @RequestMapping("/amazon/electronics")
    public InvertIndexEntity electronics(){
        List<Electronics> electronics = elecRep.sampleList();
        InvertIndex index = new InvertIndex();
        electronics.stream().forEach(e ->{
            InvertIndex.Data data = new InvertIndex.Data(EngineItemType.ELECTRONICS.getId(),
                    e.getId(), (float) Math.random());
            index.add(data);
        });
        InvertIndexEntity entity = new InvertIndexEntity();
        entity.setKey("toplist_electronics");
        entity.setData(index);

        return repository.save(entity);
    }
}

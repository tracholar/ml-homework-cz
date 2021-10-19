package com.tracholar.demo.engine.api.render;

import com.tracholar.demo.api.Item;
import com.tracholar.demo.data.amazon.Electronics;
import com.tracholar.demo.data.amazon.ElectronicsRepository;
import com.tracholar.demo.data.baidu.Baike;
import com.tracholar.demo.data.baidu.BaikeRepository;
import com.tracholar.demo.engine.api.IRender;
import com.tracholar.demo.engine.engine.IEngineItem;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * @author zuoyuan
 * @date 2021/9/30 16:42
 */
@Component
public class BaikeRender implements IRender {
    @Autowired
    private BaikeRepository rep;

    @Override
    public List<Item> render(List<IEngineItem> items) {
        List<Long> idList = items.stream().map(e -> e.getId())
                .collect(Collectors.toList());
        Iterable<Baike> electronics = rep.findAllById(idList);
        Map<Long, IEngineItem> map = new HashMap<>();
        for(IEngineItem item:items){
            map.put(item.getId(), item);
        }
        List<Item> responseItems = new LinkedList<>();
        for(Baike e : electronics){
            Item item = map.get(e.getId()).toApiItem();
            item.setDetail(e);
            responseItems.add(item);
        }
        return new LinkedList<>(responseItems);
    }
}

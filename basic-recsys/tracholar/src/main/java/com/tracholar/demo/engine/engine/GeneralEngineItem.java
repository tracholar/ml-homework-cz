package com.tracholar.demo.engine.engine;

import com.tracholar.demo.api.Item;
import lombok.Data;

/**
 * @author zuoyuan
 * @date 2021/9/29 15:21
 */
@Data
public class GeneralEngineItem extends Item implements IEngineItem{
    private EngineItemType type;
    private long id;

    @Override
    public Item toApiItem() {
        return this;
    }
}

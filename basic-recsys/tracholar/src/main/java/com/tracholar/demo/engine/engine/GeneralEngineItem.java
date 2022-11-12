package com.tracholar.demo.engine.engine;

import com.tracholar.demo.api.Item;
import com.tracholar.demo.engine.api.IRender;
import lombok.Data;

/**
 * @author zuoyuan
 * @date 2021/9/29 15:21
 */
public class GeneralEngineItem extends Item implements IEngineItem{
    @Override
    public Item toApiItem() {
        return this;
    }

    @Override
    public String uniqueId() {
        return String.format("%s-%s", getType(), getId());
    }

    @Override
    public int hashCode() {
        return uniqueId().hashCode();
    }

    @Override
    public boolean equals(Object o) {
        if(!(o instanceof GeneralEngineItem)){
            return false;
        }
        return uniqueId().equals(((GeneralEngineItem) o).uniqueId());
    }
}
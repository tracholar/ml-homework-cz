package com.tracholar.demo.engine.engine;

import lombok.Data;

/**
 * @author zuoyuan
 * @date 2021/9/29 15:21
 */
@Data
public class GeneralEngineItem implements IEngineItem{
    private EngineItemType type;
    private long id;
    private float score;
}

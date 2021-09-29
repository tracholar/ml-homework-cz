package com.tracholar.demo.engine.engine;

import lombok.Getter;

/**
 * @author zuoyuan
 * @date 2021/9/29 15:16
 */
@Getter
public enum EngineItemType {
    ARTICLE(1, "文章");

    private int id;
    private String name;

    private EngineItemType(int id, String name){
        this.id = id;
        this.name = name;
    }

    public static EngineItemType fromId(int id){
        for(EngineItemType t : values()){
            if(t.getId() == id){
                return t;
            }
        }
        return null;
    }
}

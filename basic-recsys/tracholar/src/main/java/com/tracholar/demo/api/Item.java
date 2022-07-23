package com.tracholar.demo.api;

import com.tracholar.demo.engine.engine.EngineItemType;
import lombok.Data;

import java.io.Serializable;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:28
 *
 * 推荐的item
 */
@Data
public class Item implements Serializable, Comparable<Item> {
    private EngineItemType type;
    private long id;
    /**
     * 排序分
     */
    private float score;

    private IDetail detail;

    @Override
    public int compareTo(Item o) {
        if(o == null){
            return 1;
        }
        return Float.compare(score, o.score);
    }


}

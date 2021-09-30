package com.tracholar.demo.engine.engine;

import com.tracholar.demo.api.Item;
import com.tracholar.demo.engine.api.IRender;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:49
 *
 * 推荐引擎返回的item
 */
public interface IEngineItem {
    /**
     * item 类型
     * @return
     */
    EngineItemType getType();

    /**
     * 获取对应的ID
     * @return
     */
    long getId();

    /**
     * 获取引擎打分
     * @return
     */
    float getScore();

    /**
     * 设置打分
     * @param score
     */
    void setScore(float score);

    /**
     * 转换为API层的item
     * @return
     */
    Item toApiItem();
}

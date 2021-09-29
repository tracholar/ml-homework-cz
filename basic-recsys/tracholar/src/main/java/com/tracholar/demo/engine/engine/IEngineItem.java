package com.tracholar.demo.engine.engine;

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
}

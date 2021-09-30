package com.tracholar.demo.engine.api;

import com.tracholar.demo.api.Item;
import com.tracholar.demo.engine.engine.EngineItemType;
import com.tracholar.demo.engine.engine.IEngineItem;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:46
 *
 * 渲染接口
 */
public interface IRender {
    /**
     * 将引擎返回的item列表渲染成API的响应item列表
     * @param items
     * @return
     */
    List<Item> render(List<IEngineItem> items);
}

package com.tracholar.demo.api;

import lombok.Data;

import java.io.Serializable;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:28
 *
 * 推荐的item
 */
@Data
public class Item implements Serializable {
    /**
     * 排序分
     */
    private float score;
}

package com.tracholar.demo.engine.api;

import com.tracholar.demo.api.Item;
import com.tracholar.demo.api.Response;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:54
 */
@Builder
@Getter
public class ApiResponse implements Response {
    private List<Item> results;
}

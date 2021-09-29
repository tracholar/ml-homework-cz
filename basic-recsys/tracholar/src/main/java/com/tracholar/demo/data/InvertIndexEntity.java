package com.tracholar.demo.data;

import com.google.gson.Gson;
import lombok.Data;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

/**
 * @author zuoyuan
 * @date 2021/9/29 15:28
 *
 * 倒排索引
 */
@Data
@Entity
public class InvertIndexEntity {
    @Id
    @Column(name = "key", nullable = false)
    private String key;

    private String data;

    private static Gson gson = new Gson();
    public InvertIndex getData() {
        return gson.fromJson(this.data, InvertIndex.class);
    }
    public void setData(InvertIndex data){
        this.data = gson.toJson(data);
    }
}

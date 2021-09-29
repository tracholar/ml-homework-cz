package com.tracholar.demo.data;

import com.tracholar.demo.api.Item;
import lombok.Data;

import javax.persistence.*;
import java.sql.Date;

/**
 * @author zuoyuan
 * @date 2021/9/29 14:42
 */
@Data
@Entity
public class Article implements Item {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;
    private String title;
    private String content;
    private String headPic;
    private String url;
    private String author;
    private Date pubDate;
}

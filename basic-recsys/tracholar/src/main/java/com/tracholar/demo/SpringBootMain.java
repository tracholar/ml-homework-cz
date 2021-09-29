package com.tracholar.demo;

import com.tracholar.demo.data.*;
import com.tracholar.demo.engine.engine.EngineItemType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.sql.Date;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/28 19:31
 */
@SpringBootApplication
@RestController
public class SpringBootMain {
    @GetMapping("/")
    public String index(){
        return "<a href=\"#\">recsys</a>";
    }

    @Autowired
    private InvertIndexEntityRepository repository;
    @GetMapping("/test")
    public InvertIndexEntity test(){
        InvertIndex index = new InvertIndex();
        index.add(new InvertIndex.Data(EngineItemType.ARTICLE.getId(), 1, 0.21f));
        index.add(new InvertIndex.Data(EngineItemType.ARTICLE.getId(), 2, 0.1f));
        index.add(new InvertIndex.Data(EngineItemType.ARTICLE.getId(), 3, 0.1f));

        System.out.println(index);

        InvertIndexEntity entity = new InvertIndexEntity();
        entity.setData(index);
        entity.setKey("toplist");

        System.out.println(entity);
        return repository.save(entity);
    }

    public static void main(String[] args){
        SpringApplication.run(SpringBootMain.class, args);
    }
}

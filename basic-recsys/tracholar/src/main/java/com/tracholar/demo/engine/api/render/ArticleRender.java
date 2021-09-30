package com.tracholar.demo.engine.api.render;

import com.tracholar.demo.api.Item;
import com.tracholar.demo.data.Article;
import com.tracholar.demo.data.ArticleRepository;
import com.tracholar.demo.engine.api.IRender;
import com.tracholar.demo.engine.engine.IEngineItem;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:58
 */
@Component
public class ArticleRender implements IRender {
    @Autowired
    private ArticleRepository repository;

    @Override
    public List<Item> render(List<IEngineItem> items) {
        List<Long> idList = items.stream().map(e -> e.getId())
                .collect(Collectors.toList());
        Iterable<Article> articles = repository.findAllById(idList);

        Map<Long, IEngineItem> map = new HashMap<>();
        for(IEngineItem item:items){
            map.put(item.getId(), item);
        }
        List<Item> responseItems = new LinkedList<>();
        for(Article article : articles){
            article.setScore(map.get(article.getId()).getScore());
            responseItems.add(article);
        }
        responseItems.sort((o1, o2) -> - o1.compareTo(o2));
        return new LinkedList<>(responseItems);
    }
}

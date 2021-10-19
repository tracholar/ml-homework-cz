package com.tracholar.demo.data;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

public interface ArticleRepository extends CrudRepository<Article, Long> {
    @Query(value = "select * from article where hash(id) % 10 = 1 limit 100",
            nativeQuery = true)
    Iterable<Article> sample();
}
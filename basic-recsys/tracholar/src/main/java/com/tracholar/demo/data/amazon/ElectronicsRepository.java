package com.tracholar.demo.data.amazon;

import com.tracholar.demo.data.Article;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface ElectronicsRepository extends CrudRepository<Electronics, Long> {
    @Query(value = "select * from Electronics limit 10", nativeQuery = true)
    List<Electronics> sampleList();

    @Query(value = "select * from electronics where random() % 10 =1 limit 100",
            nativeQuery = true)
    Iterable<Electronics> sample();
}
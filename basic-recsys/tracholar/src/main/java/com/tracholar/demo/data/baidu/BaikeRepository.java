package com.tracholar.demo.data.baidu;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

public interface BaikeRepository extends CrudRepository<Baike, Long> {
    @Query(value = "select * from baike limit 10", nativeQuery = true)
    Iterable<Baike> sample();

}
package com.tracholar.demo.data.amazon;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface ReviewRepository extends CrudRepository<Review, Long> {
    @Query(value = "select * from Review limit 10", nativeQuery = true)
    List<Review> sampleList();
}
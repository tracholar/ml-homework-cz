package com.tracholar.demo.data;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface FeatureEntityRepository
        extends CrudRepository<FeatureEntity, String>, CustomFeatureQuery{
}

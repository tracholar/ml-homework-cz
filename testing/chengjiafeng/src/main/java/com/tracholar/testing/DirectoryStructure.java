package com.tracholar.testing;

import java.io.File;

/**
 * Created by zuoyuan on 2019/7/19.
 */
public class DirectoryStructure {
    public boolean create(String directoryPath) {
        File directory = new File(directoryPath);

        if(directory.exists()){
            throw new IllegalArgumentException(directoryPath + " already exists.");
        }

        return directory.mkdirs();
    }
}

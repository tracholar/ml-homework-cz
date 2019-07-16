package com.tracholar.flink.demo

import java.util.Properties

import org.apache.flink.streaming.api.TimeCharacteristic
import org.apache.flink.streaming.api.scala._

/**
  * Created by zuoyuan on 2019/7/12.
  */
object KafkaConnectorDemo {
	def main(args: Array[String]) {
		val env = StreamExecutionEnvironment.getExecutionEnvironment
		env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)

		val properties = new Properties()
		properties.setProperty("bootstrap.servers", "localhost:9092")
		// only required for Kafka 0.8
		properties.setProperty("zookeeper.connect", "localhost:2181")
		properties.setProperty("group.id", "test")

	}
}

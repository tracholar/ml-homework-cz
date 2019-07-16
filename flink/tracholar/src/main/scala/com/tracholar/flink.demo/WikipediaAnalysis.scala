package com.tracholar.flink.demo

import org.apache.flink.api.common.functions.AggregateFunction
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.time.Time
import org.apache.flink.streaming.connectors.wikiedits.{WikipediaEditEvent, WikipediaEditsSource}
import org.apache.flink.streaming.api.scala.extensions._

/**
  * Created by zuoyuan on 2019/7/8.
  */
object WikipediaAnalysis {
	def main(args: Array[String]) {
		val env = StreamExecutionEnvironment.getExecutionEnvironment
		val edits = env.socketTextStream("localhost", 1025)
		val result = edits.flatMap(line => line.split("\\s+"))
			.map((_, 1)).keyBy(0)
		    .timeWindow(Time.seconds(5))
		    .sum(1)
		result.writeAsText("output/result")

		env.execute()

	}
}

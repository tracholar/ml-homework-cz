package com.tracholar.flink.demo

import org.apache.flink.api.common.functions.AggregateFunction
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.time.Time
import org.apache.flink.streaming.connectors.wikiedits.{WikipediaEditEvent, WikipediaEditsSource}
import org.apache.flink.streaming.api.scala.extensions._

/**
  * Created by zuoyuan on 2019/7/8.
  */
object DataStreamApiDemo {
	def main(args: Array[String]) {
		val env = StreamExecutionEnvironment.getExecutionEnvironment
		val edits = env.socketTextStream("localhost", 1025)
		// TODO 实现stream的分窗统计,统计每个词出现的次数, 你可能需要了解datastrteam api https://ci.apache.org/projects/flink/flink-docs-release-1.8/dev/datastream_api.html
		val counts = edits.flatMap(_.toLowerCase.split("\\W+").filter(_.nonEmpty)).map((_, 1))
			.keyBy(0).timeWindow(Time.seconds(5)).sum(1)
		counts.print()
		env.execute("Job name.")
	}
}

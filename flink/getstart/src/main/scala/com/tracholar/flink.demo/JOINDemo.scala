package com.tracholar.flink.demo

import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.streaming.api.TimeCharacteristic
import org.apache.flink.streaming.api.functions.source.RichParallelSourceFunction
import org.apache.flink.streaming.api.functions.source.SourceFunction.SourceContext
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.watermark.Watermark
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows
import org.apache.flink.streaming.api.windowing.time.Time

/**
  * Created by zuoyuan on 2019/7/9.
  */
object JOINDemo {
	def main(args: Array[String]) {
		val env = StreamExecutionEnvironment.getExecutionEnvironment
		env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)

		val stream = env.addSource(new DataSource)
		val stream2 = env.addSource(new DataSource)

		//TODO 实现两个stream的JOIN操作

	}

	private class DataSource extends RichParallelSourceFunction[(Long, Long)] {
		@volatile private var running = true

		override def run(ctx: SourceContext[(Long, Long)]): Unit = {
			// TODO 实现数据生产逻辑
		}

		override def cancel(): Unit = running = false
	}
}

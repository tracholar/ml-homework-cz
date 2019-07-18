package com.tracholar.flink.demo

import org.apache.flink.api.common.functions.AggregateFunction
import org.apache.flink.streaming.api.functions.sink.SinkFunction
import org.apache.flink.streaming.api.functions.source.RichParallelSourceFunction
import org.apache.flink.streaming.api.functions.source.SourceFunction.SourceContext
import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.streaming.api.windowing.time.Time
import org.apache.flink.api.scala._
import org.apache.flink.streaming.api.windowing.assigners.{EventTimeSessionWindows, SlidingEventTimeWindows, TumblingEventTimeWindows}
import org.apache.flink.streaming.api.windowing.evictors.Evictor
import org.apache.flink.streaming.api.windowing.windows.TimeWindow
/**
  * Created by zuoyuan on 2019/7/8.
  */
object CustomDataSourceExample {

	def main(args: Array[String]) {
		val env = StreamExecutionEnvironment.getExecutionEnvironment
		env.setParallelism(4)

		val stream = env.addSource(new DataSource)
		// TODO 自定义数据源, 实现简单的分窗统计
	}

	private class DataSource extends RichParallelSourceFunction[(Long, Long)] {
		@volatile private var running = true

		override def run(ctx: SourceContext[(Long, Long)]): Unit = {
			// TODO 实现数据生产逻辑
		}

		override def cancel(): Unit = running = false
	}
}

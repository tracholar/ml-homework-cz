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
import org.apache.flink.streaming.api.watermark.Watermark

/**
  * Created by zuoyuan on 2019/7/8.
  */
object CustomDataSourceExample {

	def main(args: Array[String]) {
		val env = StreamExecutionEnvironment.getExecutionEnvironment
		env.setParallelism(4) //并行4个流

		val stream = env.addSource(new DataSource)
		// TODO 自定义数据源, 实现简单的分窗统计
		val counts = stream.map((_, 1))
			.keyBy(0).timeWindow(Time.seconds(3)).sum(1)
		counts.print()
		env.execute("Job name.")

	}

	private class DataSource extends RichParallelSourceFunction[(Long, Long)] {
		@volatile private var running = true
		var rand = scala.util.Random
		override def run(ctx: SourceContext[(Long, Long)]): Unit = {
			// TODO 实现数据生产逻辑
			while(true) {
				val next: (Long, Long) = (rand.nextLong() % 3, rand.nextLong() % 3)
				ctx.collectWithTimestamp(next, System.currentTimeMillis())
				ctx.emitWatermark(new Watermark(System.currentTimeMillis()))
				Thread.sleep(1000)
			}
		}

		override def cancel(): Unit = running = false
	}
}

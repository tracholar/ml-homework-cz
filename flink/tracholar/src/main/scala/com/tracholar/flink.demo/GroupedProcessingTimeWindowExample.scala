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
object GroupedProcessingTimeWindowExample {

	def main(args: Array[String]) {
		val env = StreamExecutionEnvironment.getExecutionEnvironment
		env.setParallelism(4)

		val stream = env.addSource(new DataSource)
		val winAss = TumblingEventTimeWindows.of(Time.seconds(5))
		val winAss2 = SlidingEventTimeWindows.of(Time.seconds(10), Time.seconds(5))
		val winAss3 = EventTimeSessionWindows.withGap(Time.minutes(10))
		val agg = new AggregateFunction[(Long, Long), (Long, Long), Double] {
			override def createAccumulator() = (0L, 0L)

			override def add(value: (Long, Long), accumulator: (Long, Long)) =
				(accumulator._1 + value._2, accumulator._2 + 1L)

			override def getResult(accumulator: (Long, Long)) = accumulator._1 / accumulator._2

			override def merge(a: (Long, Long), b: (Long, Long)) =
				(a._1 + b._1, a._2 + b._2)
		}


		stream.keyBy(0)
			.timeWindow(Time.milliseconds(2500), Time.milliseconds(500))
		    .reduce((v1, v2) => (v1._1, v1._2 + v2._2))
		    .addSink(new SinkFunction[(Long, Long)] {
				override def invoke(in : (Long, Long)) = {
					println(in)
				}
			})

		env.execute("hello")
	}

	private class DataSource extends RichParallelSourceFunction[(Long, Long)] {
		@volatile private var running = true

		override def run(ctx: SourceContext[(Long, Long)]): Unit = {
			val startTime = System.currentTimeMillis()

			val numElements = 20000000
			val numKeys = 10000
			var value = 1L
			var count = 0L

			while (running && count < numElements) {

				ctx.collect((value, 1L))

				count += 1
				value += 1

				if (value > numKeys) {
					value = 1L
				}
				Thread.sleep(10);
			}

			val endTime = System.currentTimeMillis()
			println(s"Took ${endTime - startTime} msecs for ${numElements} values")
		}

		override def cancel(): Unit = running = false
	}
}

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

		stream.join(stream2)
		    .where(_._1)
		    .equalTo(_._2)
		    .window(TumblingEventTimeWindows.of(Time.seconds(5)))
		    .apply { (a, b) => (a._1, b._2 + a._2)}
		    .print()

		env.execute(getClass.getName)

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

				ctx.collectWithTimestamp((value, 1L), System.currentTimeMillis())
				ctx.emitWatermark(new Watermark(System.currentTimeMillis() - 5000))

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

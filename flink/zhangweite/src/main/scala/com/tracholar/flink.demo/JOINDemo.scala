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
//		env.setParallelism(4)

		val stream = env.addSource(new DataSource)
		val stream2 = env.addSource(new DataSource)

		//TODO 实现两个stream的JOIN操作
		val stream3 = stream.join(stream2).where(_._1).equalTo(_._1).
			window(TumblingEventTimeWindows.of(Time.seconds(3))).apply((e1, e2) => (e1._1,e1._2, e2._2)).print()
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

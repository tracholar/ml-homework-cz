package com.tracholar.flink.demo

import org.apache.flink.api.common.state.{ValueState, ValueStateDescriptor}
import org.apache.flink.api.java.tuple.Tuple
import org.apache.flink.streaming.api.functions.KeyedProcessFunction
import org.apache.flink.streaming.api.functions.source.RichParallelSourceFunction
import org.apache.flink.streaming.api.functions.source.SourceFunction.SourceContext
import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.streaming.api.watermark.Watermark
import org.apache.flink.util.Collector
import org.apache.flink.streaming.api.scala._

import scala.util.Random

/**
 * Created by zuoyuan on 2019/7/10.
 */
object ProcessFunctionDemo {
	def main(args: Array[String]) {
		val env = StreamExecutionEnvironment.getExecutionEnvironment

		val stream = env.addSource(new DataSource)
		stream.keyBy(0).process(new CountWithTimeoutFunction)
		    .print()

		env.execute("process function demo")
	}

	case class CountWithTimestamp(key: String, count: Long, lastModified: Long)

	class CountWithTimeoutFunction extends KeyedProcessFunction[Tuple, (String, String), (String, Long)] {
		lazy val state : ValueState[CountWithTimestamp] = getRuntimeContext
		    .getState(new ValueStateDescriptor[CountWithTimestamp]("mystate", classOf[CountWithTimestamp]))

		override def processElement(
									   value: (String, String),
									   ctx: KeyedProcessFunction[Tuple, (String, String), (String, Long)]#Context,
										out: Collector[(String, Long)]): Unit = {
			val current = state.value match {
				case null => CountWithTimestamp(value._1, 1, ctx.timestamp())
				case CountWithTimestamp(key, count, lastModified) =>
					CountWithTimestamp(key, count + 1, ctx.timestamp()    )
			}
			state.update(current)
			ctx.timerService().registerEventTimeTimer(current.lastModified + 60000)
		}

		override def onTimer(timestamp: Long,
							 ctx: KeyedProcessFunction[Tuple, (String, String), (String, Long)]#OnTimerContext,
							 out: Collector[(String, Long)]) = {
			state.value match {
				case CountWithTimestamp(key, count, lastModified) if timestamp == lastModified + 60000 => out.collect((key, count))
				case _ =>
			}
		}
	}

	def rnd = Random.alphanumeric.take(10).mkString("")

	private class DataSource extends RichParallelSourceFunction[(String, String)] {
		@volatile private var running = true

		override def run(ctx: SourceContext[(String, String)]): Unit = {
			val startTime = System.currentTimeMillis()

			val numElements = 20000000
			val numKeys = 10000
			var value = 1L
			var count = 0L

			while (running && count < numElements) {

				ctx.collectWithTimestamp((rnd, rnd), System.currentTimeMillis())
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

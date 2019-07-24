package com.tracholar.flink.demo

import org.apache.flink.api.common.state.{ValueState, ValueStateDescriptor}
import org.apache.flink.api.java.tuple.Tuple
import org.apache.flink.streaming.api.TimeCharacteristic
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
		env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)

		val stream:DataStream[Tuple2[String, String]] = env.addSource(new DataSource)
		//TODO 使用 processFunction API 处理
		stream.keyBy(0).process(new CountWithTimeoutFunction()).print()
		env.execute("job name.")
	}

	//状态存储格式
	case class CountWithTimestamp(key: String, count: Long, lastModified: Long)

	class CountWithTimeoutFunction extends KeyedProcessFunction[Tuple, (String, String), (String, Long)] {

		//  该函数维护的state
		lazy val state : ValueState[CountWithTimestamp] = getRuntimeContext
		    .getState(new ValueStateDescriptor[CountWithTimestamp]("mystate", classOf[CountWithTimestamp]))

		override def processElement(
									   value: (String, String),
									   ctx: KeyedProcessFunction[Tuple, (String, String), (String, Long)]#Context,
										out: Collector[(String, Long)]): Unit = {
			// TODO 实现processElement逻辑
			// 初始化或者更新state
			val current: CountWithTimestamp = state.value match {
				case null =>
					CountWithTimestamp(value._1, 1, ctx.timestamp())
				case CountWithTimestamp(key, count, lastModified) =>
					CountWithTimestamp(key, count + 1, ctx.timestamp())
			}
			// 更新state
			state.update(current)
			// 从现在开始，规划下一个计时点
			ctx.timerService.registerEventTimeTimer(current.lastModified + 1000)
		}

		override def onTimer(
													timestamp: Long,
													ctx: KeyedProcessFunction[Tuple, (String, String), (String, Long)]#OnTimerContext,
													out: Collector[(String, Long)]): Unit = {
			// 时间满足条件时触发函数
			state.value match {
				case CountWithTimestamp(key, count, lastModified) if (timestamp == lastModified + 1000) =>
					out.collect((key, count))
				case _ =>
			}
		}
	}

	private class DataSource extends RichParallelSourceFunction[(String, String)] {
		@volatile private var running = true
		var rand = scala.util.Random

		override def run(ctx: SourceContext[(String, String)]): Unit = {
			// TODO 实现数据生产逻辑
			while(true) {
				val next: (String, String) = (""+rand.nextLong() % 3, ""+rand.nextLong() % 3)
				ctx.collectWithTimestamp(next, System.currentTimeMillis())
				ctx.emitWatermark(new Watermark(System.currentTimeMillis()))
				Thread.sleep(1000)
			}
		}

		override def cancel(): Unit = running = false
	}
}

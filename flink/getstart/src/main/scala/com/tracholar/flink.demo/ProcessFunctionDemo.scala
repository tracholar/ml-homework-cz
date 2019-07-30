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
		//TODO 使用 processFunction API 处理
	}

	case class CountWithTimestamp(key: String, count: Long, lastModified: Long)

	class CountWithTimeoutFunction extends KeyedProcessFunction[Tuple, (String, String), (String, Long)] {
		lazy val state : ValueState[CountWithTimestamp] = getRuntimeContext
			.getState(new ValueStateDescriptor[CountWithTimestamp]("mystate", classOf[CountWithTimestamp]))

		override def processElement(
																 value: (String, String),
																 ctx: KeyedProcessFunction[Tuple, (String, String), (String, Long)]#Context,
																 out: Collector[(String, Long)]): Unit = {
			// TODO 实现processElement逻辑
		}

		override def onTimer(timestamp: Long,
												 ctx: KeyedProcessFunction[Tuple, (String, String), (String, Long)]#OnTimerContext,
												 out: Collector[(String, Long)]) = {
			//TODO 实现onTimer逻辑
		}
	}

	def rnd = Random.alphanumeric.take(10).mkString("")

	private class DataSource extends RichParallelSourceFunction[(String, String)] {
		@volatile private var running = true

		override def run(ctx: SourceContext[(String, String)]): Unit = {
			// TODO 实现数据生产逻辑
		}

		override def cancel(): Unit = running = false
	}
}
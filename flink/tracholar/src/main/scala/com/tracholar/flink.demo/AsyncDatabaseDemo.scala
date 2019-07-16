package com.tracholar.flink.demo


import java.util.concurrent.TimeUnit

import org.apache.flink.runtime.concurrent.Executors
import org.apache.flink.streaming.api.functions.source.RichParallelSourceFunction
import org.apache.flink.streaming.api.functions.source.SourceFunction.SourceContext
import org.apache.flink.streaming.api.watermark.Watermark
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.scala.async.{AsyncFunction, ResultFuture}

import scala.concurrent.{ExecutionContext, Future}
import scala.util.Random
import ExecutionContext.Implicits.global

/**
  * Created by zuoyuan on 2019/7/11.
  */
object AsyncDatabaseDemo {
	def main(args: Array[String]) {
		val env = StreamExecutionEnvironment.getExecutionEnvironment

		val stream = env.addSource(new DataSource).map(_._1)

		AsyncDataStream.unorderedWait(stream, new AsyncDatabaseRequest, 1000, TimeUnit.MILLISECONDS, 100).print()

		env.execute("async database demo")
	}

	class DatabaseClient {
		def query(str: String) = Future {
			Thread.sleep(10)
			str + "--" + rnd
		}
	}
	class AsyncDatabaseRequest extends AsyncFunction[String, (String, String)] {
		lazy val client = new DatabaseClient

		implicit lazy val executor: ExecutionContext = ExecutionContext.fromExecutor(Executors.directExecutor())

		override def asyncInvoke(str: String, resultFuture: ResultFuture[(String, String)]): Unit = {
			val resultFutureReq: Future[String] = client.query(str)

			resultFutureReq.onSuccess {
				case result: String => resultFuture.complete(Iterable((str, result)))
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

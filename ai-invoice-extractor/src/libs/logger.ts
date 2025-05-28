import { env } from "@/libs/env"
import pino from "pino"

export const logger = pino({
  level: env.EXTRACTOR_DEBUG ? "debug" : "info",
  transport: {
    target: "pino-pretty",
    options: {
      colorize: true,
      ignore: "pid,hostname,time"
    }
  }
})

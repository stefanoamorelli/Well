import { env } from "@/libs/env"
import { logger } from "@/libs/logger"
import type { AiConfig } from "@/types"

/**
 * Configuration.
 */
export const config = {
  debug: env.EXTRACTOR_DEBUG,
  ai: {
    vendor: env.EXTRACTOR_VENDOR,
    model: env.EXTRACTOR_MODEL,
    apiKey: env.EXTRACTOR_API_KEY
  } as AiConfig
}

logger.debug("env config: %s", JSON.stringify(config, null, 2))

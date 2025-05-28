import { DEFAULT_MODEL_ID } from "@/constants"
import { logger } from "@/libs/logger"
import type { AiConfig } from "@/types"

export const ConfigUtils = {
  /** Merge 2 AI configs (e.g. CLI and environment variables). */
  mergeAiConfig: ({ cliAiConfig, envAiConfig }: { cliAiConfig: Partial<AiConfig>; envAiConfig: AiConfig }) => {
    const mergedAiConfig = {
      vendor: cliAiConfig.vendor ?? envAiConfig.vendor,
      model: cliAiConfig.vendor // if cli has vendor set
        ? cliAiConfig.model // and if cli has model set
          ? cliAiConfig.model // use cli model
          : DEFAULT_MODEL_ID[cliAiConfig.vendor] // otherwise use default model for vendor (e.g. mistral:open-mixtral-8x22b)
        : envAiConfig.model, // otherwise use environment model
      apiKey: cliAiConfig.apiKey ?? envAiConfig.apiKey
    } as AiConfig

    logger.debug(`env ai-config merged with cli options: ${JSON.stringify(mergedAiConfig, null, 2)}`)

    return mergedAiConfig
  }
}

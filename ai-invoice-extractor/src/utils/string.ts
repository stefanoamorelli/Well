export const StringUtils = {
  /**
   * Mask a string by showing only the last 5 characters
   * @param str - The string to mask
   * @returns The masked string
   */
  mask(str: string, firstChars = 10, lastChars = 5): string {
    if (str.length <= 20) {
      return str.padEnd(20, "*")
    }

    const firstPart = str.slice(0, firstChars)
    const lastPart = str.slice(-lastChars)
    const maskedPart = "*".repeat(5)

    return firstPart + maskedPart + lastPart
  }
}

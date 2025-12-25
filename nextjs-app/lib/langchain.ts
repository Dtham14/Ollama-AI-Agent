import { HfInference } from '@huggingface/inference'
import { PromptTemplate } from '@langchain/core/prompts'

export function getHuggingFaceClient() {
  if (!process.env.HF_TOKEN) {
    throw new Error('HF_TOKEN is not set')
  }

  return new HfInference(process.env.HF_TOKEN)
}

export function getLLM() {
  if (!process.env.HF_TOKEN) {
    throw new Error('HF_TOKEN is not set')
  }

  return new HfInference(process.env.HF_TOKEN)
}

export const chatPromptTemplate = PromptTemplate.fromTemplate(`
You are an expert in answering questions about Classical Music, including composers, their lives, works, musical periods, and styles.
Use the provided context to give accurate, detailed answers. If the context doesn't contain enough information, say so honestly.

Context: {context}

Question: {question}

Answer:`)

import { getVectorIndex } from './pinecone'
import { HfInference } from '@huggingface/inference'

const embeddingModel = 'sentence-transformers/all-MiniLM-L6-v2'

export async function generateEmbedding(text: string): Promise<number[]> {
  if (!process.env.HF_TOKEN) {
    throw new Error('HF_TOKEN is not set')
  }

  const hf = new HfInference(process.env.HF_TOKEN)

  const embedding = await hf.featureExtraction({
    model: embeddingModel,
    inputs: text,
  })

  // Handle different possible return types from HuggingFace
  if (Array.isArray(embedding)) {
    // If it's a 2D array (batch), take the first element
    if (Array.isArray(embedding[0])) {
      return embedding[0] as number[]
    }
    // If it's already a 1D array of numbers
    return embedding as number[]
  }

  // If it's a single number, wrap it in an array
  return [embedding as number]
}

export async function searchSimilarDocuments(
  query: string,
  topK: number = 4
): Promise<Array<{ id: string; score: number; metadata: any; content: string }>> {
  try {
    // Generate embedding for the query
    const queryEmbedding = await generateEmbedding(query)

    // Get Pinecone index
    const index = await getVectorIndex()

    // Search for similar vectors
    const results = await index.query({
      vector: queryEmbedding,
      topK,
      includeMetadata: true,
    })

    // Format results
    return (results.matches || []).map((match) => ({
      id: match.id,
      score: match.score || 0,
      metadata: match.metadata || {},
      content: (match.metadata?.content as string) || '',
    }))
  } catch (error) {
    console.error('Vector search error:', error)
    return []
  }
}

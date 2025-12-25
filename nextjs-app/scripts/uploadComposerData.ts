/**
 * Script to upload composer data from backend to Pinecone
 * Run with: npx tsx scripts/uploadComposerData.ts
 */

import { HfInference } from '@huggingface/inference'
import { Pinecone } from '@pinecone-database/pinecone'
import * as fs from 'fs'
import * as path from 'path'
import * as dotenv from 'dotenv'

// Load environment variables
dotenv.config()

const CHUNK_SIZE = 1000
const CHUNK_OVERLAP = 200
const BATCH_SIZE = 100

// Initialize clients
const hf = new HfInference(process.env.HF_TOKEN!)
const pinecone = new Pinecone({ apiKey: process.env.PINECONE_API_KEY! })
const index = pinecone.index(process.env.PINECONE_INDEX_NAME || 'classical-music')

async function generateEmbedding(text: string, retries = 3): Promise<number[]> {
  for (let attempt = 0; attempt < retries; attempt++) {
    try {
      const embedding = await hf.featureExtraction({
        model: 'sentence-transformers/all-MiniLM-L6-v2',
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
    } catch (error: any) {
      const isLastAttempt = attempt === retries - 1

      if (isLastAttempt) {
        throw error
      }

      // Exponential backoff: 2s, 4s, 8s
      const waitTime = Math.pow(2, attempt + 1) * 1000
      console.log(`    ⚠️  API error, retrying in ${waitTime/1000}s... (attempt ${attempt + 1}/${retries})`)
      await new Promise(resolve => setTimeout(resolve, waitTime))
    }
  }

  throw new Error('Failed to generate embedding after retries')
}

function chunkText(text: string, chunkSize: number, overlap: number): string[] {
  const chunks: string[] = []
  let start = 0

  while (start < text.length) {
    const end = Math.min(start + chunkSize, text.length)
    chunks.push(text.substring(start, end))
    start += chunkSize - overlap
  }

  return chunks
}

async function processComposerFile(filePath: string, era: string): Promise<any[]> {
  const content = fs.readFileSync(filePath, 'utf-8')
  const filename = path.basename(filePath, '.md')
  const composerName = filename.replace(/_/g, ' ')

  console.log(`  Processing ${composerName}...`)

  // Split into chunks
  const chunks = chunkText(content, CHUNK_SIZE, CHUNK_OVERLAP)
  console.log(`    Created ${chunks.length} chunks`)

  // Generate embeddings and prepare vectors
  const vectors = []
  for (let i = 0; i < chunks.length; i++) {
    const chunk = chunks[i]
    const embedding = await generateEmbedding(chunk)

    vectors.push({
      id: `${filename}_chunk_${i}`,
      values: embedding,
      metadata: {
        composer: composerName,
        era,
        source: `${composerName} Biography`,
        content: chunk,
        chunkIndex: i,
        totalChunks: chunks.length,
      },
    })

    // Show progress
    if ((i + 1) % 10 === 0) {
      console.log(`    Generated embeddings: ${i + 1}/${chunks.length}`)
    }

    // Rate limiting: small delay between requests
    await new Promise(resolve => setTimeout(resolve, 100))
  }

  return vectors
}

async function uploadToPinecone(vectors: any[]) {
  console.log(`\nUploading ${vectors.length} vectors to Pinecone...`)

  // Upload in batches
  for (let i = 0; i < vectors.length; i += BATCH_SIZE) {
    const batch = vectors.slice(i, i + BATCH_SIZE)
    await index.upsert(batch)
    console.log(`  Uploaded batch ${Math.floor(i / BATCH_SIZE) + 1}/${Math.ceil(vectors.length / BATCH_SIZE)}`)
  }
}

async function main() {
  console.log('🎵 Classical Music Data Upload to Pinecone\n')

  // Path to composer sources (in backend directory)
  const composerSourcesDir = path.join(__dirname, '../../backend/data/composer_sources')

  if (!fs.existsSync(composerSourcesDir)) {
    console.error(`❌ Composer sources directory not found: ${composerSourcesDir}`)
    process.exit(1)
  }

  // Get all era directories
  const eras = fs.readdirSync(composerSourcesDir).filter((item) => {
    const fullPath = path.join(composerSourcesDir, item)
    return fs.statSync(fullPath).isDirectory()
  })

  console.log(`Found ${eras.length} musical eras\n`)

  let allVectors: any[] = []
  let totalFiles = 0

  // Process each era
  for (const era of eras) {
    console.log(`📁 Processing ${era} era...`)
    const eraPath = path.join(composerSourcesDir, era)
    const files = fs.readdirSync(eraPath).filter((f) => f.endsWith('.md'))

    console.log(`  Found ${files.length} composer files`)

    for (const file of files) {
      const filePath = path.join(eraPath, file)
      const vectors = await processComposerFile(filePath, era)
      allVectors = allVectors.concat(vectors)
      totalFiles++
    }

    console.log(`✓ Completed ${era} era\n`)
  }

  console.log(`\n📊 Summary:`)
  console.log(`  Total composers: ${totalFiles}`)
  console.log(`  Total chunks: ${allVectors.length}`)

  // Upload all vectors to Pinecone
  await uploadToPinecone(allVectors)

  console.log(`\n✅ Upload complete!`)
  console.log(`   ${allVectors.length} vectors uploaded to Pinecone`)
}

main().catch((error) => {
  console.error('❌ Error:', error)
  process.exit(1)
})

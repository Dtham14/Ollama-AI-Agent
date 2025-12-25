import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getLLM, chatPromptTemplate } from '@/lib/langchain'
import { searchSimilarDocuments } from '@/lib/vectorSearch'
import type { ChatRequest, ChatResponse, SourceCitation } from '@/types'

export async function POST(request: NextRequest) {
  try {
    const body: ChatRequest = await request.json()
    const { message, sessionId } = body

    if (!message) {
      return NextResponse.json({ error: 'Message is required' }, { status: 400 })
    }

    // Create or get session
    let session
    if (sessionId) {
      session = await prisma.session.findUnique({ where: { id: sessionId } })
      if (!session) {
        return NextResponse.json({ error: 'Session not found' }, { status: 404 })
      }
    } else {
      // Create new session
      session = await prisma.session.create({
        data: {
          title: message.substring(0, 50) + (message.length > 50 ? '...' : ''),
        },
      })
    }

    // Save user message
    await prisma.message.create({
      data: {
        sessionId: session.id,
        role: 'user',
        content: message,
      },
    })

    // Search for relevant documents
    const relevantDocs = await searchSimilarDocuments(message, 4)

    // Format context from relevant documents
    const context = relevantDocs
      .map((doc) => doc.content)
      .join('\n\n')

    // Generate response using HuggingFace Inference API
    const hf = getLLM()
    const model = process.env.DEFAULT_MODEL || 'meta-llama/Llama-3.2-3B-Instruct'

    const systemPrompt = `You are an expert in answering questions about Classical Music, including composers, their lives, works, musical periods, and styles.
Use the provided context to give accurate, detailed answers. If the context doesn't contain enough information, say so honestly.

Context: ${context || 'No specific context available.'}`

    const result = await hf.chatCompletion({
      model,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: message },
      ],
      max_tokens: 512,
      temperature: 0.7,
    })

    const response = result.choices[0]?.message?.content || 'Sorry, I could not generate a response.'

    // Format sources
    const sources: SourceCitation[] = relevantDocs.map((doc) => ({
      source: doc.metadata.source || 'Unknown',
      content: doc.content.substring(0, 200) + '...',
      score: doc.score,
    }))

    // Save assistant message
    await prisma.message.create({
      data: {
        sessionId: session.id,
        role: 'assistant',
        content: response,
        sources: JSON.stringify(sources),
      },
    })

    // Update session message count and timestamp
    await prisma.session.update({
      where: { id: session.id },
      data: {
        messageCount: { increment: 2 }, // user + assistant
        updatedAt: new Date(),
      },
    })

    const chatResponse: ChatResponse = {
      response,
      sessionId: session.id,
      sources,
    }

    return NextResponse.json(chatResponse)
  } catch (error) {
    console.error('Chat error:', error)
    return NextResponse.json(
      { error: 'Failed to process message',  details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    )
  }
}

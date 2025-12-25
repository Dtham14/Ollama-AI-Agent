import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

// GET /api/chat/history/[sessionId] - Get chat history for a session
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ sessionId: string }> }
) {
  try {
    const { sessionId } = await params
    const messages = await prisma.message.findMany({
      where: { sessionId },
      orderBy: { createdAt: 'asc' },
    })

    // Parse sources JSON for each message
    const formattedMessages = messages.map((msg) => ({
      ...msg,
      sources: msg.sources ? JSON.parse(msg.sources) : null,
    }))

    return NextResponse.json(formattedMessages)
  } catch (error) {
    console.error('Error fetching chat history:', error)
    return NextResponse.json(
      { error: 'Failed to fetch chat history' },
      { status: 500 }
    )
  }
}

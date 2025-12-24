# New Features Added

## 1. Individual Message Deletion ✅

### What it does:
Delete individual messages from your chat history without deleting the entire conversation.

### How to use:
1. Hover over any message (user or assistant) in the chat
2. A trash icon will appear on the right side
3. Click the trash icon
4. Confirm deletion
5. The message is removed from both the UI and database

### Implementation details:
- **Backend**: New DELETE endpoint at `/api/chat/message/{message_id}`
- **Frontend**: Delete button appears on hover for each message
- **Database**: Message is permanently deleted and session message count is updated

---

## 2. Folder-Based PDF Training 📚

### What it does:
Bulk process multiple PDFs at once by placing them in a folder, instead of uploading one-by-one through the UI.

### How to use:

#### Step 1: Add your PDFs
Place your music theory PDFs in:
```
backend/data/training_docs/
```

Supported formats:
- PDF (`.pdf`)
- Word (`.docx`)
- Text (`.txt`)
- Markdown (`.md`)
- CSV (`.csv`)

#### Step 2: Run the training script
From the `backend` directory:
```bash
python train_from_folder.py
```

#### Step 3: Wait for processing
The script will:
- Scan for all supported documents
- Skip already processed files
- Extract text from each document
- Split into chunks (1000 chars with 200 overlap)
- Embed using `mxbai-embed-large` model
- Store in ChromaDB vector database

### Output example:
```
====================================================================
🎵 Music Theory Knowledge Base - Bulk Training Tool
====================================================================

📁 Training folder: C:\...\backend\data\training_docs

📚 Found 5 documents to process

📄 Processing: music-theory-basics.pdf
   ✅ Processed successfully! (42 chunks)
📄 Processing: chord-progressions.pdf
   ✅ Processed successfully! (35 chunks)
⏭️  Skipping (already processed): scales-and-modes.pdf
...

====================================================================
📊 Summary:
   ✅ Processed: 2
   ⏭️  Skipped: 3
   ❌ Errors: 0
   📚 Total: 5
====================================================================
```

### Force reprocessing:
If you've updated a document and want to reprocess it:
```bash
python train_from_folder.py --force
```

### Notes:
- Maximum file size: 10MB per document
- Duplicate files are automatically skipped (unless using `--force`)
- All documents are tagged as "bulk_import" for tracking
- Documents are tracked in the database to avoid reprocessing

---

## When to use UI vs Folder:

### Use **UI Upload** when:
- Adding a single document
- You want to provide custom metadata (category, tags, description)
- You prefer a visual interface

### Use **Folder Training** when:
- Bulk importing many documents at once
- Setting up initial knowledge base
- Scripting/automation
- Batch updates

---

## Technical Details

### Backend Changes:
- `app/routers/chat.py` - Added DELETE `/api/chat/message/{message_id}` endpoint
- `app/services/chat_service.py` - Added `delete_message()` method
- `train_from_folder.py` - New bulk training script

### Frontend Changes:
- `services/chatApi.ts` - Added `deleteMessage()` API call
- `stores/chatStore.ts` - Added `deleteMessage()` state action
- `components/chat/ChatMessage.tsx` - Added delete button with hover state

### Database:
- Message deletions update session message count
- All processed documents are tracked to avoid duplicates

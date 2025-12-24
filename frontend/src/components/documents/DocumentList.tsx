import React from 'react';
import { File, Trash2, RefreshCw, CheckCircle, AlertCircle, Clock, Loader2 } from 'lucide-react';
import { useDocumentStore } from '../../stores/documentStore';
import type { DocumentMetadata } from '../../types/document';
import { cn } from '../../utils/cn';

export const DocumentList: React.FC = () => {
  const { documents, isLoading, loadDocuments, deleteDocument } = useDocumentStore();

  React.useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  const handleDelete = async (documentId: string) => {
    if (confirm('Are you sure you want to delete this document?')) {
      try {
        await deleteDocument(documentId);
      } catch (error) {
        console.error('Failed to delete document:', error);
      }
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getStatusIcon = (status: DocumentMetadata['embedded']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle size={16} className="text-green-600" />;
      case 'processing':
        return <Loader2 size={16} className="text-primary-600 animate-spin" />;
      case 'failed':
        return <AlertCircle size={16} className="text-red-600" />;
      default:
        return <Clock size={16} className="text-gray-400" />;
    }
  };

  const getStatusText = (status: DocumentMetadata['embedded']) => {
    switch (status) {
      case 'completed':
        return 'Embedded';
      case 'processing':
        return 'Processing...';
      case 'failed':
        return 'Failed';
      default:
        return 'Pending';
    }
  };

  if (isLoading && documents.length === 0) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="animate-spin text-gray-400" size={32} />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">
          Uploaded Documents ({documents.length})
        </h2>
        <button
          onClick={loadDocuments}
          disabled={isLoading}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50"
          title="Refresh"
        >
          <RefreshCw size={18} className={cn('text-gray-600', isLoading && 'animate-spin')} />
        </button>
      </div>

      {documents.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <File size={48} className="mx-auto mb-4 text-gray-300" />
          <p>No documents uploaded yet</p>
          <p className="text-sm mt-1">Upload documents to expand the knowledge base</p>
        </div>
      ) : (
        <div className="space-y-2">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className="flex items-start gap-3 p-4 bg-white border border-gray-200 rounded-lg hover:shadow-sm transition-shadow"
            >
              <File size={20} className="text-gray-400 mt-1 flex-shrink-0" />

              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-gray-900 truncate">
                      {doc.original_filename}
                    </h3>
                    <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
                      <span>{doc.file_type.toUpperCase()}</span>
                      <span>•</span>
                      <span>{formatFileSize(doc.file_size)}</span>
                      <span>•</span>
                      <span>{doc.chunk_count} chunks</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handleDelete(doc.id)}
                    className="p-1.5 hover:bg-red-50 rounded transition-colors flex-shrink-0"
                    title="Delete document"
                  >
                    <Trash2 size={16} className="text-red-600" />
                  </button>
                </div>

                <div className="flex items-center gap-2 mt-2">
                  {getStatusIcon(doc.embedded)}
                  <span className="text-xs text-gray-600">
                    {getStatusText(doc.embedded)}
                  </span>
                </div>

                {doc.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {doc.tags.map((tag, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 bg-primary-50 text-primary-700 text-xs rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}

                <p className="text-xs text-gray-400 mt-2">
                  Uploaded {formatDate(doc.uploaded_at)}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
